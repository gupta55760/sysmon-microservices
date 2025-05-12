import asyncio
import aiohttp
import json
import os
import time
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Load config file
with open("config.json") as f:
    config = json.load(f)

# Recursively resolve __ENV__ values
def resolve(value):
    if isinstance(value, str) and value.startswith("__ENV__:"):
        return os.getenv(value.split(":")[1])
    elif isinstance(value, dict):
        return {k: resolve(v) for k, v in value.items()}
    elif isinstance(value, list):
        return [resolve(v) for v in value]
    else:
        return value

LOGIN_URL = config["login_url"]
FEEDBACK_URL = config["feedback_url"]
USERNAME = resolve(config["username"])
PASSWORD = resolve(config["password"])
NUM_REQUESTS = config["num_requests"]
CONCURRENCY = config["concurrency"]
payload = resolve(config["payload"])
pg_config = resolve(config["postgres"])  # resolved for completeness

async def get_jwt_token(session):
    async with session.post(LOGIN_URL, json={"username": USERNAME, "password": PASSWORD}) as resp:
        if resp.status == 200:
            data = await resp.json()
            return data.get("access_token")
        else:
            text = await resp.text()
            raise Exception(f"Login failed: {resp.status} - {text}")

async def post_feedback(session, sem, idx, headers):
    async with sem:
        start = time.perf_counter()
        async with session.post(FEEDBACK_URL, json=payload, headers=headers) as response:
            elapsed = time.perf_counter() - start
            status = response.status
            text = await response.text()
            print(f"[{idx}] Status: {status} | Time: {elapsed:.2f}s | Response: {text[:60]}")
            return status, elapsed

async def main():
    sem = asyncio.Semaphore(CONCURRENCY)
    async with aiohttp.ClientSession() as session:
        token = await get_jwt_token(session)
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        tasks = [post_feedback(session, sem, i + 1, headers) for i in range(NUM_REQUESTS)]
        results = await asyncio.gather(*tasks)

    success = sum(1 for status, _ in results if status == 200)
    total_time = sum(t for _, t in results)
    avg_time = total_time / NUM_REQUESTS

    print(f"\n✅ {success}/{NUM_REQUESTS} requests succeeded")
    print(f"📈 Avg response time: {avg_time:.2f}s")

if __name__ == "__main__":
    asyncio.run(main())
