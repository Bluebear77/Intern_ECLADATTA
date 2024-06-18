import pandas as pd

# List of input CSV files
input_files = ['qtsumm_dev.csv', 'qtsumm_test.csv', 'qtsumm_train.csv']

# Read and concatenate all CSV files
dataframes = [pd.read_csv(file) for file in input_files]
combined_df = pd.concat(dataframes)

# Remove duplicates based on all columns
combined_df = combined_df.drop_duplicates()

# Sort the combined dataframe by 'overall_similarity' in ascending order
sorted_df = combined_df.sort_values(by='overall_similarity')

# Select the 10 unique instances with the lowest 'overall_similarity'
lowest_df = sorted_df.head(10)

# Save the resulting dataframe to 'lowest.csv'
lowest_df.to_csv('lowest.csv', index=False)

print("The lowest.csv file has been generated with the 10 unique instances with the lowest overall similarity.")
