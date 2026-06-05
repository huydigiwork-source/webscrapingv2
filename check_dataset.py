from datasets import load_dataset

DATASET_NAME = "Vincentran/careerviet-accounting-jobs"

ds = load_dataset(DATASET_NAME, split="train")

print(ds)
print("TOTAL ROWS:", len(ds))

print("\nSAMPLE:")
print(ds[0])