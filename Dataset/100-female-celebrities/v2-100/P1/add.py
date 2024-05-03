import pandas as pd

# Adjusted path to the CSV files
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

# Move the 'File Name' column to be the second column in the dataframe
file_name = merged_df.pop('File Name')
merged_df.insert(1, 'File Name', file_name)

# Sort the DataFrame by extracting numbers from 'File Name' and sorting numerically
merged_df['File Number'] = merged_df['File Name'].str.extract('(\d+)').astype(float)
merged_df.sort_values(by='File Number', inplace=True)
merged_df.drop('File Number', axis=1, inplace=True)  # Drop the temporary sorting column

# Save the updated dataframe to a new CSV file
merged_df.to_csv('numerically_sorted_updated_100-female-celebrities.csv', index=False)
