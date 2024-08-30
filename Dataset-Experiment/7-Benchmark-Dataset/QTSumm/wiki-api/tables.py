import pandas as pd

# Load the CSV files
dev_df = pd.read_csv('qtsumm_dev.csv')
test_df = pd.read_csv('qtsumm_test.csv')
train_df = pd.read_csv('qtsumm_train.csv')

# Get unique table_ids for each dataframe
unique_dev = dev_df['table_id'].nunique()
unique_test = test_df['table_id'].nunique()
unique_train = train_df['table_id'].nunique()

# Combine all table_ids to get the total unique count across all files
combined_unique = pd.concat([dev_df['table_id'], test_df['table_id'], train_df['table_id']]).nunique()

# Print the results
print(f"Number of unique tables in qtsumm_dev.csv: {unique_dev}")
print(f"Number of unique tables in qtsumm_test.csv: {unique_test}")
print(f"Number of unique tables in qtsumm_train.csv: {unique_train}")
print(f"Total number of unique tables across all three CSV files: {combined_unique}")
