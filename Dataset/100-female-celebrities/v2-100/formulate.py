import os
import json

def process_file(input_path, output_path):
    try:
        with open(input_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except json.JSONDecodeError:
        print(f"Error decoding JSON from file: {input_path}")
        return

    processed_data = []
    for dataset in data.get('tableData', []):
        if not dataset:
            continue

        header = dataset[0]
        rows = dataset[1:]

        processed_data.append({
            "id": data.get("id", ""),
            "title": data.get("title", ""),
            "url": data.get("url", [""])[0] if data.get("url") else "",
            "header": header,
            "rows": rows,
            "column_types": "",  # placeholder for column types
            "key_column": "",  # placeholder for key column
            "numeric_columns": [],
            "date_columns": {}
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
