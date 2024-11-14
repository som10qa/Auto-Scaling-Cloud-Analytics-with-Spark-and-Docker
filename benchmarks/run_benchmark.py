from pyspark.sql import SparkSession
import time
import psutil
import pandas as pd
import os

start_time = time.time()
# Initialize Spark Session
spark = SparkSession.builder.appName("Performance Benchmarking Airline Delay").getOrCreate()

# Define the path to data and output
data_folder_path = "/opt/spark-data/"
output_excel_path = "/opt/spark-data/Airline_Delay_Benchmark_Output.xlsx"

# List of years to process
years = [str(year) for year in range(2009, 2018)]

# Function to log CPU and memory utilization
def log_resource_utilization():
    cpu_usage = psutil.cpu_percent()
    memory_info = psutil.virtual_memory()
    return cpu_usage, memory_info.percent

# Function to process each year and log resource usage
def process_year(year):
    file_path = os.path.join(data_folder_path, f"{year}.csv")
    df = spark.read.csv(file_path, header=True, inferSchema=True)

    # Persist the DataFrame to avoid redundant computation (RDD coupling)
    df.persist()

    # Calculate average delay per airline
    avg_delay = df.groupBy("OP_CARRIER").agg({"DEP_DELAY": "avg"})
    avg_delay.persist()  # Persist this RDD to avoid recomputation
    avg_delay_pd = avg_delay.toPandas()

    # Calculate total delay per day and airline
    total_delay = df.groupBy("FL_DATE", "OP_CARRIER").agg({"ARR_DELAY": "sum"})
    total_delay.persist()  # Persist this RDD as well
    total_delay_pd = total_delay.toPandas()

    # Unpersist DataFrames after converting to Pandas to free memory
    avg_delay.unpersist()
    total_delay.unpersist()
    df.unpersist()

    return year, avg_delay_pd, total_delay_pd

# Start benchmarking
start_time = time.time()
cpu_log, memory_log = [], []

results = []
for year in years:
    year, avg_delay_pd, total_delay_pd = process_year(year)
    results.append((year, avg_delay_pd, total_delay_pd))

    # Log resource utilization after each year's processing
    cpu, memory = log_resource_utilization()
    cpu_log.append(cpu)
    memory_log.append(memory)
    print(f"Year {year} processed - CPU: {cpu}%, Memory: {memory}%")

end_time = time.time()
total_duration = end_time - start_time
print(f"Total Benchmarking Time: {total_duration:.2f} seconds")

# Save logs to output
log_df = pd.DataFrame({"Year": years, "CPU_Usage": cpu_log, "Memory_Usage": memory_log})
log_df.to_csv("/opt/spark-data/benchmark_results.csv", index=False)

# Save results to Excel
with pd.ExcelWriter(output_excel_path, engine="openpyxl") as writer:
    for year, avg_delay_pd, total_delay_pd in results:
        avg_delay_pd.to_excel(writer, sheet_name=f"Avg_Delay_{year}", index=False)
        total_delay_pd.to_excel(writer, sheet_name=f"Total_Delay_{year}", index=False)

# Stop Spark session
spark.stop()
end_time = time.time()
print(f"Job completed in {end_time - start_time} seconds")