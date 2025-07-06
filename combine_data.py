import pandas as pd
import glob

# Get all CSV files in the directory
csv_files = glob.glob("*.csv")

# Initialize an empty list to store DataFrames
df_list = []

for i, file in enumerate(csv_files):
    if i == 0:
        # Read the first file normally (with headers)
        df = pd.read_csv(file)
        
    else:
        # Read other files without headers (skip the first row)
        df = pd.read_csv(file, skiprows=1, header=None)
        # Set column names to match the first file
        df.columns = df_list[0].columns
    
    print(f"file {i} done")
    df_list.append(df)

# Concatenate all DataFrames
combined_df = pd.concat(df_list, ignore_index=True)

# Save the combined DataFrame
combined_df.to_csv("combined_output.csv", index=False)

print(f"Combined {len(csv_files)} CSV files into 'combined_output.csv'.")
