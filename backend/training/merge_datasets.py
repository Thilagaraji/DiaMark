import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

file1 = os.path.abspath(os.path.join(BASE_DIR, "../../trained_features/combined_features.csv"))
file2 = os.path.abspath(os.path.join(BASE_DIR, "../../trained_features/dataset_features.csv"))

output_file = os.path.abspath(os.path.join(BASE_DIR, "../../trained_features/final_dataset.csv"))

print("Loading datasets...")

df1 = pd.read_csv(file1)
df2 = pd.read_csv(file2)

print("Dataset 1:", df1.shape)
print("Dataset 2:", df2.shape)

# 🔥 IMPORTANT: Align columns
df2 = df2[df1.columns]

# Combine
final_df = pd.concat([df1, df2], ignore_index=True)

# Shuffle
final_df = final_df.sample(frac=1, random_state=42).reset_index(drop=True)

# Save
final_df.to_csv(output_file, index=False)

print("✅ Final dataset saved:", output_file)
print("Final shape:", final_df.shape)