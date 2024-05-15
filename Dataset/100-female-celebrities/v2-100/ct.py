import os
import json
import csv


extraction_dir = './P4/'

# Create a directory to extract the files
os.makedirs(extraction_dir, exist_ok=True)


# List all the files in the extraction directory
extracted_files = os.listdir(extraction_dir)

# Define the output CSV file path
output_csv_path = 'column_types.csv'

# Prepare a list to hold the rows for the CSV
csv_rows = []
files_with_only_unknown = []

# Function to recursively search for column_types in nested dictionaries or lists, and record the file name
def find_column_types_with_filename(data, file_name):
    if isinstance(data, dict):
        for key, value in data.items():
            if key == 'column_types' and isinstance(value, list):
                for column_type in value:
                    csv_rows.append([file_name, column_type])
            else:
                find_column_types_with_filename(value, file_name)
    elif isinstance(data, list):
        for item in data:
            find_column_types_with_filename(item, file_name)

# Iterate through each JSON file and extract column_types along with the file name
for file_name in extracted_files:
    if file_name.endswith('.json'):
        file_path = os.path.join(extraction_dir, file_name)
        with open(file_path, 'r') as file:
            data = json.load(file)
            find_column_types_with_filename(data, file_name)

# Sort the rows by file name
csv_rows.sort(key=lambda x: int(x[0].split('_')[1]))

# Identify files with only "UNKNOWN" column type
file_column_types = {}
for row in csv_rows:
    file_name, column_type = row
    if file_name not in file_column_types:
        file_column_types[file_name] = set()
    file_column_types[file_name].add(column_type)

for file_name, column_types in file_column_types.items():
    if column_types == {"UNKNOWN"}:
        files_with_only_unknown.append(file_name)

# Write the collected data to a CSV file
with open(output_csv_path, 'w', newline='') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['file_name', 'column_type'])  # Write the header
    writer.writerows(csv_rows)  # Write the data

# Print the files with only "UNKNOWN" column type
print("Files with only 'UNKNOWN' column type:")
for file in files_with_only_unknown:
    print(file)

print(f"CSV file has been created at: {output_csv_path}")