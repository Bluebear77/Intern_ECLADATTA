import os
import json
from datetime import datetime

# Function to determine if a value is numeric
def is_numeric(value):
    try:
        float(value)
        return True
    except (ValueError, TypeError):
        return False

# Function to determine if a value is datetime
def is_datetime(value):
    try:
        datetime.fromisoformat(value)
        return True
    except (ValueError, TypeError):
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

# Function to ensure column_types matches the length of header
def ensure_column_types_length(data):
    if 'header' in data and 'column_types' in data:
        header_length = len(data['header'])
        column_types_length = len(data['column_types'])
        
        if column_types_length < header_length:
            data['column_types'].extend(['string'] * (header_length - column_types_length))
        elif column_types_length > header_length:
            data['column_types'] = data['column_types'][:header_length]

# Function to recursively search for column_types in nested dictionaries or lists, and refine them
def find_and_refine_column_types(data):
    numeric_columns = []
    date_columns = {}
    
    if isinstance(data, dict):
        if 'header' in data and 'column_types' in data:
            ensure_column_types_length(data)
        for key, value in data.items():
            if key == 'column_types' and isinstance(value, list):
                refined_column_types = []
                for idx, col_type in enumerate(value):
                    column_values = [row[idx] for row in data.get('rows', []) if len(row) > idx]
                    refined_type = convert_column_type(col_type, column_values)
                    refined_column_types.append(refined_type)
                    if refined_type == 'numeric':
                        numeric_columns.append(idx)
                    elif refined_type == 'datetime':
                        date_columns[idx] = column_values
                data['column_types'] = refined_column_types
                data['numeric_columns'] = numeric_columns
                data['date_columns'] = date_columns
            else:
                find_and_refine_column_types(value)
    elif isinstance(data, list):
        for item in data:
            find_and_refine_column_types(item)



# Set input and output directories
input_dir = './P3'
output_processed_dir = './P4'

# Create the output directory if it doesn't exist
if not os.path.exists(output_processed_dir):
    os.makedirs(output_processed_dir)

# Process each JSON file in the input directory
for file_name in os.listdir(input_dir):
    if file_name.endswith('_v3.json'):
        input_file_path = os.path.join(input_dir, file_name)
        output_file_name = file_name.replace('_v3.json', '_v4.json')
        output_file_path = os.path.join(output_processed_dir, output_file_name)
        try:
            with open(input_file_path, 'r') as file:
                data = json.load(file)
                
                # Ensure the column types length is correct before refining
                ensure_column_types_length(data)
                
                find_and_refine_column_types(data)

                # Write the processed data to the output directory
                with open(output_file_path, 'w') as outfile:
                    json.dump(data, outfile, ensure_ascii=False, indent=4)
            print(f"Processed {file_name} successfully.")
        except Exception as e:
            print(f"Error processing {file_name}: {e}")
