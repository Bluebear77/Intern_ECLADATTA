import json
import os
import glob
from dateutil.parser import parse
from datetime import datetime

def read_json_file(json_path):
    with open(json_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def is_date(string):
    try:
        # More stringent checks for date-like strings
        result = parse(string, fuzzy=False)
        # Ensure the parsed date is reasonable, for example between year 1000 and 3000
        if 1000 <= result.year <= 3000:
            return True
        return False
    except (ValueError, OverflowError):
        return False

def looks_numeric(s):
    try:
        # Handles more general numeric detection without causing int conversion issues
        float(s.replace(',', '').replace('.', '').strip())
        return True
    except ValueError:
        return False

def process_table_data(data):
    processed_data = []
    for table in data["tableData"]:
        if not table:
            continue
        header = table[0]
        rows = table[1:]
        column_types = ['string'] * len(header)
        numeric_columns = []
        date_columns = {}

        for col_index, column in enumerate(header):
            numeric_count = 0
            date_count = 0
            total_count = 0

            for row in rows:
                if len(row) > col_index:
                    value = row[col_index].strip()
                    if looks_numeric(value):
                        numeric_count += 1
                    if is_date(value):
                        date_count += 1
                    total_count += 1

            if total_count == 0:
                continue

            if numeric_count == total_count:
                column_types[col_index] = "numeric"
                numeric_columns.append(col_index)
            elif date_count > 0.5 * total_count:
                column_types[col_index] = "datetime"
                date_columns[col_index] = [row[col_index] for row in rows if len(row) > col_index]

        key_column = numeric_columns[0] if numeric_columns else next(iter(date_columns), -1)

        dataset = {
            "id": data["id"],
            "title": data["title"],
            "url": data["url"],
            "header": header,
            "rows": rows,
            "column_types": column_types,
            "key_column": key_column,
            "numeric_columns": numeric_columns,
            "date_columns": date_columns
        }
        processed_data.append(dataset)
    return processed_data

def process_json_file(json_path, output_path):
    data = read_json_file(json_path)
    processed_data = process_table_data(data)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(processed_data, f, ensure_ascii=False, indent=4)

def process_directory(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for json_file in glob.glob(os.path.join(input_dir, '*.json')):
        base_filename = os.path.basename(json_file)
        output_file_path = os.path.join(output_dir, base_filename)
        process_json_file(json_file, output_file_path)
        print(f'Processed {json_file} and saved the results to {output_file_path}')

# Example usage
input_dir = 'P1'
output_dir = 'P2'
process_directory(input_dir, output_dir)
