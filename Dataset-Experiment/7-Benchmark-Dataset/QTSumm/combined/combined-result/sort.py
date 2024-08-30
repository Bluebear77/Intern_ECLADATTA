import pandas as pd
import os

# List of input CSV files
input_files = ['qtsumm_test_sorted.csv', 'qtsumm_dev_sorted.csv', 'qtsumm_train_sorted.csv']

for input_file in input_files:
    # Read the CSV file
    df = pd.read_csv(input_file)
    
    # Remove duplicate rows based on the 'title' column
    df_cleaned = df.drop_duplicates(subset=['title'])
    
    # Define the output file path in the current directory
    output_file = os.path.basename(input_file)
    
    # Save the cleaned DataFrame to the output file
    df_cleaned.to_csv(output_file, index=False)
    
    print(f"Processed {input_file}, saved cleaned data to {output_file}")

# Loop through each output file, sort by 'overall_similarity', and update it
for output_file in input_files:
    # Read the cleaned CSV file
    df = pd.read_csv(output_file)
    
    # Sort the DataFrame by 'overall_similarity'
    df_sorted = df.sort_values(by='overall_similarity', ascending=True)
    
    # Save the sorted DataFrame back to the same file
    df_sorted.to_csv(output_file, index=False)
    
    print(f"Sorted {output_file} by 'overall_similarity' and updated the file")

print("All files processed, sorted, and saved successfully.")
