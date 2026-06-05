import pandas as pd

df = pd.read_parquet("jobs.parquet")

print("Rows:", len(df))
print(df.head())