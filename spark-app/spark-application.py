from pyspark.sql import SparkSession
from pyspark.sql.functions import avg, col

# Initialize Spark session
spark = SparkSession.builder \
    .appName("AirlineDelayAnalysis") \
    .master("spark://spark-master:7077") \
    .getOrCreate()

# Load the dataset
df = spark.read.option("header", "true").csv("/opt/spark-data/airline_delay.csv")

# Convert delay columns to numeric
df = df.withColumn("ArrivalDelay", col("ArrDelay").cast("integer")) \
       .withColumn("DepartureDelay", col("DepDelay").cast("integer"))

# Example 1: Calculate average arrival delay per airline
avg_arrival_delay = df.groupBy("Airline") \
                      .agg(avg("ArrivalDelay").alias("AvgArrivalDelay")) \
                      .orderBy("AvgArrivalDelay", ascending=False)
avg_arrival_delay.show()

# Example 2: Calculate total cancellations per airport
cancellations_per_airport = df.filter(df["Cancelled"] == "1") \
                              .groupBy("Origin") \
                              .count() \
                              .orderBy("count", ascending=False)
cancellations_per_airport.show()

# Example 3: Calculate delays by month
delays_by_month = df.groupBy("Month") \
                    .agg(avg("DepartureDelay").alias("AvgDepartureDelay"), 
                         avg("ArrivalDelay").alias("AvgArrivalDelay"))
delays_by_month.show()

# Stop the Spark session
spark.stop()