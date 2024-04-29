import os
import json

def read_json_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        return json.load(file)

def write_json_file(data, filepath):
    with open(filepath, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)

def merge_datasets(p1_dir, p4_dir, output_dir):
    p1_files = [f for f in os.listdir(p1_dir) if f.endswith('.json')]
    p4_files = [f for f in os.listdir(p4_dir) if f.endswith('.json')]

    missing_matches = []

    for p1_file in p1_files:
        instance_number = p1_file.split('_')[-1]  # Extract instance number from filename
        p4_file = f'cleaned_output_instance_{instance_number}'

        if p4_file in p4_files:
            p1_data = read_json_file(os.path.join(p1_dir, p1_file))
            p4_data = read_json_file(os.path.join(p4_dir, p4_file))

            dataset = {
                "id": p1_data["ID"],
                "title": p1_data["Title"],
                "url": p1_data["URLs"][0],  # Assuming we use the first URL
                "header": p4_data[0]["header"],
                "rows": p4_data[0]["rows"],
                "column_types": ["string"] + ["numeric"]*(len(p4_data[0]["header"]) - 1),
                "key_column": 0,
                "numeric_columns": list(range(1, len(p4_data[0]["header"]))),
                "date_columns": {}
            }

            # Save each merged dataset to a separate file
            output_file_path = os.path.join(output_dir, f'merged_output_{instance_number}')
            write_json_file(dataset, output_file_path)
        else:
            missing_matches.append(instance_number)

    # Report missing matches
    if missing_matches:
        print("No matching P4 files for the following P1 instances:", ", ".join(missing_matches))

# Set directories
p1_directory = 'P1'
p4_directory = 'P4'
output_directory = 'P5'

merge_datasets(p1_directory, p4_directory, output_directory)
