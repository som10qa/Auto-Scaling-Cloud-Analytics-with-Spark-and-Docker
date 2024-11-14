import os
import time
import subprocess

def scale_workers(target_count):
    subprocess.call(["docker-compose", "scale", f"spark-worker={target_count}"])

def monitor_and_scale():
    while True:
        # Mock CPU usage check
        cpu_usage = get_cpu_usage()  # Placeholder for actual monitoring logic
        worker_count = get_current_worker_count()

        if cpu_usage > 80 and worker_count < max_workers:
            scale_workers(worker_count + 1)
        elif cpu_usage < 30 and worker_count > min_workers:
            scale_workers(worker_count - 1)
        
        time.sleep(60)

def get_cpu_usage():
    # Placeholder for actual CPU usage logic
    return 50  # Mock value for initial testing

def get_current_worker_count():
    result = subprocess.check_output("docker ps -q -f name=spark-worker", shell=True)
    return len(result.splitlines())

if __name__ == "__main__":
    max_workers = 5
    min_workers = 1
    monitor_and_scale()