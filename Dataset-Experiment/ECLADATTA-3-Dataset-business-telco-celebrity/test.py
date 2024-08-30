import os
import json
from datetime import datetime

# Set input and output directories
input_dir = 'telco-100/Raw'
output_dir = 'telco-100/result'

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

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

def is_numeric(value):
    try:
        float(value)
        return True
    except (ValueError, TypeError):
        return False

def is_datetime(value):
    try:
        datetime.fromisoformat(value)
        return True
    except (ValueError, TypeError):
        return False

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

def find_and_refine_column_types(data):
    numeric_columns = []
    date_columns = {}
    
    if isinstance(data, dict):
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

def process_file(i):
    input_file_path = f'{input_dir}/instance_{i}.json'
    processed_file_path = f'{output_dir}/instance_{i}_result.json'
    
    # Check if input file exists
    if not os.path.exists(input_file_path):
        print(f"Skipping instance_{i} as input file does not exist.")
        return
    
    try:
        # Read the input instance_i.json
        with open(input_file_path, 'r', encoding='utf-8') as file:
            instance_data = json.load(file)

        # Extract primaryKeyPosition and typingLabel from preprocessingMetadata
        preprocessing_metadata = instance_data['_source'].get('preprocessingMetadata', [])
        primary_key_position = None
        typing_label = []

        for tech_result in preprocessing_metadata:
            if 'technologyResults' in tech_result:
                tech_results = tech_result['technologyResults']
                for result in tech_results:
                    if ('dagobah' in result and 
                        'preprocessed' in result['dagobah'] and
                        'primaryKeyInfo' in result['dagobah']['preprocessed']):
                        
                        preprocessed = result['dagobah']['preprocessed']
                        primary_key_position = preprocessed['primaryKeyInfo'].get('primaryKeyPosition')
                        typing_label = [label['typing'][0]['typingLabel'] for label in preprocessed['primitiveTyping']]
                        break
                if primary_key_position is not None:
                    break

        # Sanity check to ensure the keys are found
        if primary_key_position is None or not typing_label:
            print(f"Skipping instance_{i} due to missing primaryKeyPosition or typingLabel.")
            return

        # Update all tables in the data
        for table in instance_data['tables']:
            table['key_column'] = primary_key_position
            table['column_types'] = [convert_typing_label(label) for label in typing_label]

        # Refine column types
        find_and_refine_column_types(instance_data['tables'])

        # Process date columns
        processed_data = process_date_columns(instance_data['tables'])

        # Ensure output directory exists
        os.makedirs(os.path.dirname(processed_file_path), exist_ok=True)

        # Save the updated data to instance_i_result.json
        with open(processed_file_path, 'w', encoding='utf-8') as file:
            json.dump(processed_data, file, ensure_ascii=False, indent=4)

        print(f"Processed and saved file to {processed_file_path}")

    except Exception as e:
        print(f"Error processing instance_{i}: {e}")

# Process files from 1 to 100
for i in range(1, 101):
    process_file(i)
