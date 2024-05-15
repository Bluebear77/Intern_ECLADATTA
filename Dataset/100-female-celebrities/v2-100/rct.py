import os
import json
from datetime import datetime

# Function to determine if a value is numeric
def is_numeric(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

# Function to determine if a value is datetime
def is_datetime(value):
    try:
        datetime.fromisoformat(value)
        return True
    except ValueError:
        return False

# Function to convert the column type
def convert_column_type(column_type, value):
    if column_type == 'UNKNOWN':
        if isinstance(value, list):
            if all(is_numeric(v) for v in value):
                return 'numeric'
            elif all(is_datetime(v) for v in value):
                return 'datetime'
            else:
                return 'string'
        else:
            if is_numeric(value):
                return 'numeric'
            elif is_datetime(value):
                return 'datetime'
            else:
                return 'string'
    else:
        if column_type in ['CARDINAL', 'ORDINAL', 'PERCENT', 'RANGE', 'TIME']:
            return 'numeric'
        elif column_type in ['datetime']:
            return 'datetime'
        else:
            return 'string'

# Function to recursively search for column_types in nested dictionaries or lists, and refine them
def find_and_refine_column_types(data):
    if isinstance(data, dict):
        for key, value in data.items():
            if key == 'column_types' and isinstance(value, list):
                refined_column_types = [convert_column_type(col_type, value) for col_type in value]
                data[key] = refined_column_types
            else:
                find_and_refine_column_types(value)
    elif isinstance(data, list):
        for item in data:
            find_and_refine_column_types(item)

# Set input and output directories
input_dir = './P4'
output_dir = './P5'

# Create the output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Process each JSON file in the input directory
for file_name in os.listdir(input_dir):
    if file_name.endswith('.json'):
        input_file_path = os.path.join(input_dir, file_name)
        output_file_path = os.path.join(output_dir, file_name)

        with open(input_file_path, 'r') as file:
            data = json.load(file)
            find_and_refine_column_types(data)

            # Write the processed data to the output directory
            with open(output_file_path, 'w') as outfile:
                json.dump(data, outfile, ensure_ascii=False, indent=4)

# Check the first few output files to verify
print(os.listdir(output_dir)[:5])
