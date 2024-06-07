import pandas as pd
import json
import os

# Load the below_threshold.csv file
csv_file = 'below_threshold.csv'
df_below_threshold = pd.read_csv(csv_file)

# Get the list of table_ids from the CSV file
table_ids = df_below_threshold['table_id'].tolist()

# Load the merged_qtsumm.json file
json_file = '../merged_qtsumm.json'
with open(json_file, 'r') as f:
    data = json.load(f)

# Filter the instances based on the table_id
filtered_instances = [instance for instance in data if instance['table']['table_id'] in table_ids]

# Save the filtered instances to a new JSON file
output_file = 'filtered_qtsumm.json'
with open(output_file, 'w') as f:
    json.dump(filtered_instances, f, indent=4)

print(f"Filtered {len(filtered_instances)} instances based on table_id and saved to {output_file}")
