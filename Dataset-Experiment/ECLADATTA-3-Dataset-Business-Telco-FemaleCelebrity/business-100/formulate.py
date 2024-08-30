import os
import json
from datetime import datetime

def infer_data_types(row):
    types = []
    for item in row:
        try:
            int(item)
            types.append('numeric')
        except ValueError:
            try:
                datetime.strptime(item, '%Y-%m-%d')
                types.append('datetime')
            except ValueError:
                types.append('string')
    return types

def process_file(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    processed_data = []
    for dataset in data['tableData']:
        if not dataset:
            continue

        header = dataset[0]
        rows = dataset[1:]
        column_types = infer_data_types(rows[0]) if rows else ['string'] * len(header)

        numeric_columns = [i for i, typ in enumerate(column_types) if typ == 'numeric']
        date_columns = {i: [row[i] for row in rows] for i, typ in enumerate(column_types) if typ == 'datetime'}

        processed_data.append({
            "id": data["id"],
            "title": data["title"],
            "url": data["url"][0] if data["url"] else "",
            "header": header,
            "rows": rows,
            "column_types": column_types,
            "key_column": 0,  # assuming the first column is the key column
            "numeric_columns": numeric_columns,
            "date_columns": date_columns
        })

    with open(output_path, 'w', encoding='utf-8') as file:
        json.dump(processed_data, file, ensure_ascii=False, indent=4)

def process_directory(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(input_dir):
        input_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, os.path.splitext(filename)[0] + '_processed.json')
        process_file(input_path, output_path)

# Example usage
input_dir = 'P1'
output_dir = 'P2'
process_directory(input_dir, output_dir)
