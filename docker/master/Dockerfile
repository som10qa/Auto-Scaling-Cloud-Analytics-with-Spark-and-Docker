# Use the official Spark image
FROM apache/spark:latest

# Install additional packages
USER root
RUN apt-get update && \
    apt-get install -y procps iputils-ping curl netcat && \
    rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV SPARK_HOME=/opt/spark
ENV PATH=$SPARK_HOME/bin:$PATH

# Copy the startup script for Spark Worker
COPY scripts/start-master.sh /opt/spark/scripts/start-master.sh
RUN chmod +x /opt/spark/scripts/start-master.sh
RUN pip install pandas openpyxl pyspark psutil

# Expose the necessary ports for Spark Worker
EXPOSE 8081

# Start the Spark Worker process
ENTRYPOINT ["/opt/spark/scripts/start-master.sh"]
