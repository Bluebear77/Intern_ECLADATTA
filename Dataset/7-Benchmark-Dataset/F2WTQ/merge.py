import pandas as pd

# File paths
file1 = 'complete-F2WTQ_test_data_fetaqa_form_500tables.csv'
file2 = 'complete-F2WTQ_test_data_processed.csv'
file3 = 'complete-F2WTQ_validation_data_processed.csv'

# Read the CSV files
df1 = pd.read_csv(file1)
df2 = pd.read_csv(file2)
df3 = pd.read_csv(file3)

# Concatenate the dataframes
merged_df = pd.concat([df1, df2, df3], ignore_index=True)

# Save the merged dataframe to a new CSV file
merged_df.to_csv('F2WTQ.csv', index=False)
