#!/bin/bash

# Number of retries to connect to Spark Master
RETRIES=10
SLEEP_INTERVAL=10  # Seconds between retries

# Spark Master URL (use environment variable or default to spark-master:7077)
SPARK_MASTER_URL=${SPARK_MASTER_URL:-"spark://spark-master:7077"}

echo "Starting Spark Worker with Spark Master URL: $SPARK_MASTER_URL"

# Optional: Add a manual entry to /etc/hosts if DNS resolution issues occur
echo "$(getent hosts spark-master | awk '{ print $1 }') spark-master" >> /etc/hosts

# Loop to wait for Spark Master Web UI to become available on port 8080
while [ $RETRIES -gt 0 ]; do
  if curl -s "http://spark-master:8080" > /dev/null; then
    echo "Connected to Spark Master Web UI at http://spark-master:8080"
    break
  else
    echo "Waiting for Spark Master Web UI to be available... ($RETRIES retries left)"
    RETRIES=$((RETRIES-1))
    sleep $SLEEP_INTERVAL
  fi
done

# Exit if Spark Master is not reachable after retries
if [ $RETRIES -eq 0 ]; then
  echo "Spark Master is not reachable. Exiting."
  exit 1
fi

# Start the Spark Worker and connect to the Spark Master
echo "Starting Spark Worker and connecting to Spark Master..."
$SPARK_HOME/bin/spark-class org.apache.spark.deploy.worker.Worker "$SPARK_MASTER_URL"

# Keep the container running by tailing the worker log
tail -f $SPARK_HOME/logs/spark--org.apache.spark.deploy.worker.Worker-*.out