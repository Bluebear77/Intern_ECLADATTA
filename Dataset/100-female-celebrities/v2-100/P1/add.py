import pandas as pd

# Path to the CSV files
output_csv_path = 'output.csv'
celebrities_csv_path = '../../v1-100/100-female-celebrities.csv'

# Read the CSV files
output_df = pd.read_csv(output_csv_path)
celebrities_df = pd.read_csv(celebrities_csv_path)

# Rename the columns to remove any accidental leading/trailing whitespace
output_df.columns = output_df.columns.str.strip()
celebrities_df.columns = celebrities_df.columns.str.strip()

# Set URL as the index for merging
output_df.set_index('URL', inplace=True)
celebrities_df.set_index('URL', inplace=True)

# Join the dataframes on the URL index
merged_df = celebrities_df.join(output_df['File Name without Extension'].rename('File Name'), how='left')

# Reset index to turn the URL back into a column
merged_df.reset_index(inplace=True)

# Save the updated dataframe to a new CSV file
merged_df.to_csv('updated_100-female-celebrities.csv', index=False)
