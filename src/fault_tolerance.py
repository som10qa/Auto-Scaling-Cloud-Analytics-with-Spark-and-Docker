import subprocess
import time
import os

def check_worker_health():
    try:
        # Check for any exited (failed) Spark worker containers
        result = subprocess.check_output("docker ps -q -f name=spark-worker --filter 'status=exited'", shell=True).decode().splitlines()
        
        # Restart each failed container
        for container_id in result:
            if container_id:
                restart_failed_worker(container_id.strip())
    except subprocess.CalledProcessError as e:
        print(f"Error checking worker health: {e}")

def restart_failed_worker(container_id):
    try:
        subprocess.call(["docker", "start", container_id])
        print(f"Restarted failed Spark worker container: {container_id}")
    except subprocess.CalledProcessError as e:
        print(f"Error restarting container {container_id}: {e}")

if __name__ == "__main__":
    # Set the health check interval (default to 30 seconds)
    interval = int(os.getenv("HEALTH_CHECK_INTERVAL", 30))

    print(f"Starting fault tolerance monitoring with interval={interval} seconds.")
    
    while True:
        check_worker_health()
        time.sleep(interval)