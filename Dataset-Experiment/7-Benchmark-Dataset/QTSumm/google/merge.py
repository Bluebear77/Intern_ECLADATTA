import os
import pandas as pd

def merge_csv_files(directory, output_filename):
    # List all files in the directory
    files = os.listdir(directory)
    
    

    # Filter and sort the files that match the pattern `chunk_i.csv`
    csv_files = sorted([f for f in files if f.endswith('.csv') and '_chunk_' in f], 
                   key=lambda x: int(x.split('_chunk_')[1].split('.')[0]))


    # Initialize an empty DataFrame
    merged_df = pd.DataFrame()
    
    # Read and concatenate each CSV file
    for file in csv_files:
        file_path = os.path.join(directory, file)
        df = pd.read_csv(file_path)
        merged_df = pd.concat([merged_df, df], ignore_index=True)
    
    # Save the merged DataFrame to the output file
    merged_df.to_csv(output_filename, index=False)
    print(f'Merged file saved as {output_filename}')

# Define the directories and output filenames
directories = {
    './train': 'qtsumm_train.csv',
    './test': 'qtsumm_test.csv',
    './dev': 'qtsumm_dev.csv'
}

# Merge files for each directory
for dir_path, output_file in directories.items():
    merge_csv_files(dir_path, output_file)
