import os
import pandas as pd

def merge_and_sort_csv_files(output_file):
    # List to hold all data
    all_data = []
    
    # Iterate over all files in the current directory
    for file in os.listdir('.'):
        if file.endswith('.csv'):
            # Read the CSV file into a DataFrame
            df = pd.read_csv(file)
            all_data.append(df)
    
    # Concatenate all DataFrames into a single DataFrame
    merged_df = pd.concat(all_data)
    
    # Sort the DataFrame by 'Template Name'
    sorted_df = merged_df.sort_values(by='Template Name')
    
    # Write the sorted DataFrame to a new CSV file
    sorted_df.to_csv(output_file, index=False)

# Usage
output_file = 'merged_sorted_templates.csv'
merge_and_sort_csv_files(output_file)
