import pandas as pd

# List of input files
input_files = ['qtsumm_dev_sorted.csv', 'qtsumm_test_sorted.csv', 'qtsumm_train_sorted.csv']

# Directory for the output file
output_dir = './manual'
output_file = f'{output_dir}/manual-verified-v2.csv'

# Create an empty DataFrame to hold the combined rows
combined_df = pd.DataFrame()

# Loop through each input file and extract the first 20 rows (excluding the header)
for file in input_files:
    df = pd.read_csv(file)
    first_20_rows = df.iloc[0:20]  
    combined_df = pd.concat([combined_df, first_20_rows], ignore_index=True)

# Save the combined DataFrame to a new CSV file
combined_df.to_csv(output_file, index=False)

print(f"Extracted rows have been saved to {output_file}")
