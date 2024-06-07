import pandas as pd
import json
import os

# Load the below_threshold.csv file
csv_file = 'below_threshold.csv'
df_below_threshold = pd.read_csv(csv_file)

# Get the list of table_ids from the CSV file
table_ids = df_below_threshold['table_id'].tolist()

# List of JSON files in the parent directory
json_files = ["../qtsumm_dev.json", "../qtsumm_test.json", "../qtsumm_train.json"]

# Initialize a list to hold all data from the JSON files
all_data = []

# Iterate through the JSON files and load the data
for json_file in json_files:
    with open(json_file, 'r') as f:
        data = json.load(f)
        all_data.extend(data)

# Filter the instances based on the table_id
filtered_instances = [instance for instance in all_data if instance['table']['table_id'] in table_ids]

# Save the filtered instances to a new JSON file
output_file = 'filtered_qtsumm.json'
with open(output_file, 'w') as f:
    json.dump(filtered_instances, f, indent=4)

print(f"Filtered {len(filtered_instances)} instances based on table_id and saved to {output_file}")
