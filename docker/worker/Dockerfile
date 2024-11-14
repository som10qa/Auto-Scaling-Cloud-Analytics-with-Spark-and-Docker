# Use the official Spark image
FROM apache/spark:latest

# Install additional packages if needed
USER root
RUN apt-get update && apt-get install -y procps && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV SPARK_HOME=/opt/spark
ENV PATH=$SPARK_HOME/bin:$PATH

# Copy the startup script for Spark Worker from your directory structure
COPY scripts/start-worker.sh /opt/spark/scripts/start-worker.sh
RUN chmod +x /opt/spark/scripts/start-worker.sh

# Expose the necessary ports for Spark Worker (e.g., 8081 for monitoring)
EXPOSE 8081

# Start the Spark Worker process
ENTRYPOINT ["/opt/spark/scripts/start-worker.sh"]