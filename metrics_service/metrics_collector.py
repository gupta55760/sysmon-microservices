import psutil
import time
import platform
import socket

def collect_metrics_forever(app):
    while True:
        app.state.latest_metrics = {
            "hostname": socket.gethostname(),
            "platform": platform.system(),
            "platform_version": platform.version(),
            "uptime_secs": time.time() - psutil.boot_time(),

            "cpu": {
                "percent": psutil.cpu_percent(interval=None),
                "cores": psutil.cpu_count(logical=True),
                "load_avg": list(psutil.getloadavg()) if hasattr(psutil, 'getloadavg') else []
            },

            "memory": {
                "total": psutil.virtual_memory().total,
                "used": psutil.virtual_memory().used,
                "percent": psutil.virtual_memory().percent,
                "available": psutil.virtual_memory().available
            },

            "disk": {
                "total": psutil.disk_usage('/').total,
                "used": psutil.disk_usage('/').used,
                "free": psutil.disk_usage('/').free,
                "percent": psutil.disk_usage('/').percent
            },

            "network": psutil.net_io_counters(pernic=False)._asdict(),

            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        }

        print("📊 Metrics collected at", app.state.latest_metrics["timestamp"])
        time.sleep(5)

