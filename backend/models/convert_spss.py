import pyreadstat
import pandas as pd
import os

# Move to project root
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

# Correct file path (your file name)
file_path = os.path.join(BASE_DIR, "dataset", "finger prints.sav")

print("Reading:", file_path)

df, meta = pyreadstat.read_sav(file_path)

print(df.head())

# Save CSV
output_path = os.path.join(BASE_DIR, "dataset", "t2dm_dataset.csv")

df.to_csv(output_path, index=False)

print("Converted to CSV successfully")
print("Saved to:", output_path)