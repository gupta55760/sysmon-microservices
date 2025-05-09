# scripts/move_test_report.py
import os
import shutil
import sys
from datetime import datetime

# Always resolve paths relative to the project root
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def move_report(suite_name, timestamp=None):
    if not timestamp:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    src_dir = os.path.join(ROOT_DIR, "tests", "reports", suite_name)
    dest_dir = os.path.join(src_dir, timestamp)
    os.makedirs(dest_dir, exist_ok=True)

    if suite_name == "selenium":
        shutil.move(os.path.join(src_dir, "report.html"), os.path.join(dest_dir, "report.html"))
        screenshots = os.path.join(ROOT_DIR, "screenshots")
        if os.path.exists(screenshots):
            shutil.move(screenshots, os.path.join(dest_dir, "screenshots"))

    elif suite_name == "playwright":
        shutil.copy(os.path.join(src_dir, "index.html"), os.path.join(dest_dir, "report.html"))
        test_results = os.path.join(ROOT_DIR, "test-results")
        if os.path.exists(test_results):
            shutil.copytree(test_results, os.path.join(dest_dir, "screenshots"), dirs_exist_ok=True)

    print(f"✅ Moved {suite_name} report to {dest_dir}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python move_test_report.py <suite_name> [timestamp]")
        sys.exit(1)

    move_report(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)

