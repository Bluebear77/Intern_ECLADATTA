import pandas as pd
import json

# Load the JSON files
with open('qtsumm_dev.json', 'r') as f:
    dev_data = json.load(f)

with open('qtsumm_test.json', 'r') as f:
    test_data = json.load(f)

with open('qtsumm_train.json', 'r') as f:
    train_data = json.load(f)

# Extract table_id from each dataset
dev_table_ids = [entry['table']['table_id'] for entry in dev_data]
test_table_ids = [entry['table']['table_id'] for entry in test_data]
train_table_ids = [entry['table']['table_id'] for entry in train_data]

# Calculate unique table_ids for each dataset
unique_dev = len(set(dev_table_ids))
unique_test = len(set(test_table_ids))
unique_train = len(set(train_table_ids))

# Combine all table_ids to get the total unique count across all files
combined_table_ids = set(dev_table_ids) | set(test_table_ids) | set(train_table_ids)
combined_unique = len(combined_table_ids)

# Write the results to tables.txt
with open('tables.txt', 'w') as f:
    f.write(f"Number of unique tables in qtsumm_dev.json: {unique_dev}\n")
    f.write(f"Number of unique tables in qtsumm_test.json: {unique_test}\n")
    f.write(f"Number of unique tables in qtsumm_train.json: {unique_train}\n")
    f.write(f"Total number of unique tables across all three JSON files: {combined_unique}\n")
