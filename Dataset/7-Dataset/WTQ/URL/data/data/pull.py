import os
import pandas as pd

# List all .tsv files in the current directory
tsv_files = [f for f in os.listdir('.') if f.endswith('.tsv')]

# Process each .tsv file
for tsv_file in tsv_files:
    try:
        # Read the .tsv file into a DataFrame
        df = pd.read_csv(tsv_file, sep='\t', on_bad_lines='skip')
        
        # Ensure the required columns exist
        if 'id' not in df.columns or 'context' not in df.columns:
            print(f"Skipping file {tsv_file}: Missing required columns")
            continue
        
        # Extract relevant columns
        output_df = df[['id', 'context']].copy()
        output_df.rename(columns={'context': 'origin_file'}, inplace=True)
        
        # Create output .csv filename based on the .tsv filename
        csv_file = os.path.splitext(tsv_file)[0] + '.csv'
        
        # Write the extracted data to a .csv file
        output_df.to_csv(csv_file, index=False)
        
        print(f"Created {csv_file} from {tsv_file}")
    except Exception as e:
        print(f"Error processing {tsv_file}: {e}")
