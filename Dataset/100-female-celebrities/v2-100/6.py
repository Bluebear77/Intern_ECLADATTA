import json
import os
import glob
from dateutil.parser import parse

def read_json_file(json_path):
    with open(json_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return [data] if isinstance(data, dict) else data

def is_date(string):
    try:
        parse(string, fuzzy=False)
        return True
    except ValueError:
        return False

def looks_numeric(s):
    try:
        float(s.replace(',', '').replace('.', '').replace(' ', ''))
        return True
    except ValueError:
        return False

def process_single_table_data(table_data):
    output_table_data = {
        "id": table_data["id"],
        "title": table_data["title"],
        "url": table_data["url"],
        "header": table_data["header"],
        "rows": table_data["rows"],
        "column_types": ['string'] * len(table_data["header"]),
        "key_column": -1,
        "numeric_columns": [],
        "date_columns": {},
    }

    for col_index in range(len(table_data["header"])):
        numeric_count = 0
        date_count = 0
        total_count = 0
        
        for row in table_data["rows"]:
            if len(row) > col_index and row[col_index].strip():
                value = row[col_index]
                if looks_numeric(value):
                    numeric_count += 1
                if is_date(value):
                    date_count += 1
                total_count += 1

        if numeric_count == total_count:
            output_table_data["column_types"][col_index] = "numeric"
            output_table_data["numeric_columns"].append(col_index)
        elif date_count > 0.5 * total_count:
            output_table_data["column_types"][col_index] = "datetime"
            output_table_data["date_columns"][col_index] = []

    if output_table_data["numeric_columns"]:
        output_table_data["key_column"] = output_table_data["numeric_columns"][0]
    elif output_table_data["date_columns"]:
        output_table_data["key_column"] = next(iter(output_table_data["date_columns"]))

    return output_table_data

def process_json_file(json_path, output_path):
    data = read_json_file(json_path)
    output_data = []
    for table_data in data:
        processed_table_data = process_single_table_data(table_data)
        output_data.append(processed_table_data)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=4)

def process_directory(input_dir, output_dir):
    # Create the output directory if it does not exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Process each JSON file in the input directory
    for json_file in glob.glob(os.path.join(input_dir, '*.json')):
        base_filename = os.path.basename(json_file)
        output_file_path = os.path.join(output_dir, base_filename)
        process_json_file(json_file, output_file_path)
        print(f'Processed {json_file} and saved the results to {output_file_path}')

# Example usage
input_dir = 'P5'
output_dir = 'P6'
process_directory(input_dir, output_dir)

