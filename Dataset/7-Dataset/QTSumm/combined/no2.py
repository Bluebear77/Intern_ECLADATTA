import pandas as pd
import glob

# Get a list of all files matching the pattern *_sorted.csv
file_list = glob.glob('*_sorted.csv')

# Process each file
for file_name in file_list:
    # Read the CSV file into a DataFrame
    df = pd.read_csv(file_name)
    
    # Drop duplicate rows
    df.drop_duplicates(inplace=True)
    
    # Save the cleaned DataFrame back to the CSV file
    df.to_csv(file_name, index=False)
    
    print(f"Processed file: {file_name}")

print("All files processed and duplicates removed.")
