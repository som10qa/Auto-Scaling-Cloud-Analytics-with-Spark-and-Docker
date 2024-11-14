import os
import subprocess
import time
import psutil  # Ensure psutil is installed via `pip install psutil`

# Constants for thresholds and scaling
CPU_UPPER_THRESHOLD = 15  # Adjusted temporarily for testing
CPU_LOWER_THRESHOLD = 10
MAX_WORKERS = 5
MIN_WORKERS = 2
SLEEP_INTERVAL = 60

# Function to get average CPU usage
def check_cpu_usage():
    # Calculate the average CPU usage
    return psutil.cpu_percent(interval=1)

def get_current_worker_count():
    # Get the current number of running spark-worker containers
    result = subprocess.run("docker ps -q -f name=spark-worker | wc -l", shell=True, capture_output=True, text=True)
    return int(result.stdout.strip())

def scale_workers(target_scale):
    current_scale = get_current_worker_count()
    if target_scale != current_scale:
        print(f"Scaling to {target_scale} workers (current: {current_scale})...")
        cmd = f"docker-compose -f ./config/docker-compose.yml up --scale spark-worker={target_scale} -d"
        subprocess.call(cmd, shell=True)
    else:
        print("No scaling needed. Target scale is already reached.")

def auto_scale():
    while True:
        cpu_usage = check_cpu_usage()
        current_worker_count = get_current_worker_count()
        print(f"CPU usage: {cpu_usage}%, Current worker count: {current_worker_count}")

        if cpu_usage > CPU_UPPER_THRESHOLD and current_worker_count < MAX_WORKERS:
            scale_workers(current_worker_count + 1)  # Scale up by 1
        elif cpu_usage < CPU_LOWER_THRESHOLD and current_worker_count > MIN_WORKERS:
            scale_workers(current_worker_count - 1)  # Scale down by 1

        time.sleep(SLEEP_INTERVAL)

if __name__ == "__main__":
    auto_scale()