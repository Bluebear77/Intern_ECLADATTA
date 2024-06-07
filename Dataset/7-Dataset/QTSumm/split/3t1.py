import os
import pandas as pd

# Define the order of the CSV files to merge
file_order = ['qtsumm_dev.csv', 'qtsumm_test.csv', 'qtsumm_train.csv']
output_file = 'qtsumm_complete.csv'

# Create a list to hold the DataFrames
dfs = []

# Read each CSV file in the specified order and append to the list
for file in file_order:
    if os.path.exists(file):
        df = pd.read_csv(file)
        dfs.append(df)
    else:
        print(f"Warning: {file} not found.")

# Concatenate all DataFrames
if dfs:
    combined_df = pd.concat(dfs)
    # Write the combined DataFrame to a new CSV file
    combined_df.to_csv(output_file, index=False)
    print(f"Combined CSV file saved as {output_file}")
else:
    print("No CSV files to merge.")
