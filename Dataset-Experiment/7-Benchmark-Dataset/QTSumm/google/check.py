import os
import pandas as pd

# Directory containing the .csv files
directory = './train'

# List to hold the names of empty files
empty_files = []

# Get all csv files in the directory
csv_files = [f for f in os.listdir(directory) if f.endswith('.csv')]

# Check each file for data
for file in csv_files:
    file_path = os.path.join(directory, file)
    try:
        df = pd.read_csv(file_path)
        if df.empty:
            empty_files.append(file)
    except pd.errors.EmptyDataError:
        empty_files.append(file)

# Print out the names of empty files
if empty_files:
    print("Empty CSV files:")
    for file in empty_files:
        print(file)
else:
    print("No empty CSV files found.") 