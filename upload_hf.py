from huggingface_hub import login
from datasets import Dataset
import pandas as pd
import os

HF_TOKEN = os.environ["HF_TOKEN"]

login(HF_TOKEN)

df = pd.read_parquet("jobs.parquet")

dataset = Dataset.from_pandas(df)

dataset.push_to_hub(
    "huydigiwork-source/careerviet-accounting-jobs"
)

print("Upload success")