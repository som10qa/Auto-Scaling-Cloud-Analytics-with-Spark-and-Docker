#!/bin/bash

# Set the Spark Master host
export SPARK_MASTER_HOST="0.0.0.0"

# Start the Spark Master process directly without additional flags
$SPARK_HOME/bin/spark-class org.apache.spark.deploy.master.Master --host $SPARK_MASTER_HOST --port 7077 --webui-port 8080

# Verify if the Spark Master process started successfully
if pgrep -f "org.apache.spark.deploy.master.Master" > /dev/null; then
    echo "Spark Master started successfully and is running."
else
    echo "Error: Failed to start Spark Master. Exiting."
    exit 1
fi

# Wait for a short period to ensure the log file exists before tailing
sleep 2

# Keep the container running by streaming the Spark Master log
tail -f $SPARK_HOME/logs/spark--org.apache.spark.deploy.master.Master-*.out