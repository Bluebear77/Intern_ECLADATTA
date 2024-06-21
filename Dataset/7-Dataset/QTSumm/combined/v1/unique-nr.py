import json

# List of JSON files to scan
json_files = ["../../qtsumm_dev.json", "../../qtsumm_test.json", "../../qtsumm_train.json"]

def count_unique_tables(file_path, key):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        unique_values = set()
        for item in data:
            unique_values.add(item['table'][key])
        return len(unique_values)
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
        return 0

# Process each file and print the number of unique tables
for file in json_files:
    unique_table_ids = count_unique_tables(file, 'table_id')
    unique_titles = count_unique_tables(file, 'title')
    print(f"File: {file}")
    print(f"Number of unique tables based on 'table_id': {unique_table_ids}")
    print(f"Number of unique tables based on 'title': {unique_titles}")
    print("-" * 40)
