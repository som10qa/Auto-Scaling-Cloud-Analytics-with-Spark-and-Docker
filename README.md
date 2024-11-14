# Cloud-Based Data Analytics Platform with Auto-Scaling Using Apache Spark and Docker

This project is a cloud-based data analytics platform using Apache Spark for distributed data processing and Docker for container management.

## Folder Structure
- `benchmarks/`: Contains benchmark scripts and results
- `config/`: Configuration files for Spark, Docker, and environment variables
- `data/`: Input datasets
- `docker/`: Dockerfiles and scripts for setting up Spark master and worker nodes
- `monitoring/`: Auto-scaling scripts and monitoring configurations
- `spark-app/`: Main Spark applications
- `src/`: Source code for data processing

## Running the Project
1. Start the platform with Spark master and workers:
    ```bash
    docker-compose up --scale spark-worker=3
    ```

2. To run benchmarks:
    ```bash
    python spark-app/run_benchmark.py
    ```

3. To enable auto-scaling:
    ```bash
    python monitoring/scale_monitor.py
    ```

## Dependencies
- Docker
- Docker Compose
- Apache Spark
- Python packages (pandas, openpyxl, pyspark)

## Results
The results will be saved in `data/Airline_Delay_2009_2017.xlsx`.