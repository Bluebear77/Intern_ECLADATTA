import os
import pandas as pd
import re

# Directory containing the .csv files
directory = './train'

# Function to extract the chunk number from the filename
def get_chunk_number(filename):
    match = re.search(r'qtsumm_dev_chunk_(\d+).csv', filename)
    return int(match.group(1)) if match else float('inf')

# Get all csv files in the directory
csv_files = [f for f in os.listdir(directory) if f.endswith('.csv')]

# Sort files by the chunk number
csv_files.sort(key=get_chunk_number)

# List to hold dataframes
df_list = []

# Read and append each dataframe to the list
for file in csv_files:
    file_path = os.path.join(directory, file)
    df = pd.read_csv(file_path)
    df_list.append(df)

# Concatenate all dataframes
merged_df = pd.concat(df_list)

# Save the merged dataframe to a new csv file
merged_df.to_csv(os.path.join(directory, 'train.csv'), index=False)

print("Merged CSV file created successfully.")

