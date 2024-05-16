import os
import json

# Directories
input_dir = './P5'
output_processed_dir = './P6'

# Ensure the output directory exists
os.makedirs(output_processed_dir, exist_ok=True)

def is_valid_int(value):
    try:
        int(value)
        return True
    except ValueError:
        return False

def process_date_columns(data):
    for entry in data:
        if "date_columns" in entry:
            for key, values in entry["date_columns"].items():
                entry["date_columns"][key] = [int(v) if is_valid_int(v) else 9999 for v in values]
    return data

# Process all JSON files in the input directory
for filename in os.listdir(input_dir):
    if filename.startswith('instance_') and filename.endswith('_v5.json'):
        instance_number = filename.split('_')[1]

        input_filepath = os.path.join(input_dir, filename)
        output_filename = f'instance_{instance_number}_v6.json'
        output_filepath = os.path.join(output_processed_dir, output_filename)

        # Load the data from the input file
        with open(input_filepath, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # Process the data
        processed_data = process_date_columns(data)

        # Save the processed data to the output file
        with open(output_filepath, 'w', encoding='utf-8') as file:
            json.dump(processed_data, file, ensure_ascii=False, indent=4)

print("Processing complete. Processed files are saved in the output directory.")
