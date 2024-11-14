import pandas as pd

# Load benchmark results
benchmark_results_path = "../benchmarks/output/metrics/benchmark_results.csv"
benchmark_df = pd.read_csv(benchmark_results_path)

# Load expected results (assumed to be stored in a CSV for comparison)
expected_results_path = "../benchmarks/output/metrics/expected_results.csv"  # You can create this based on the research paper results
expected_df = pd.read_csv(expected_results_path)

# Merge benchmark and expected results on filename or a common identifier
comparison_df = benchmark_df.merge(expected_df, on="file", suffixes=("_actual", "_expected"))

# Calculate differences in metrics (example: processing time)
comparison_df["processing_time_diff"] = (
    comparison_df["processing_time_actual"] - comparison_df["processing_time_expected"]
)

# Print and save the comparison
print(comparison_df)
comparison_df.to_csv("../benchmarks/output/metrics/comparison_results.csv", index=False)