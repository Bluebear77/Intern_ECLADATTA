import re
import json

def is_numeric(s):
    try:
        float(s.replace(',', '').replace(' ', ''))
        return True
    except ValueError:
        return False

def detect_column_types(rows):
    if not rows:
        return []

    num_rows_to_sample = min(5, len(rows))  # Use up to 5 rows to determine data types
    column_types = ['unknown'] * len(rows[0])

    for i in range(len(rows[0])):  # Iterate over each column
        sample_values = [row[i] for row in rows[:num_rows_to_sample]]
        if all(is_numeric(value) for value in sample_values):
            column_types[i] = 'numeric'
        else:
            column_types[i] = 'string'
    
    return column_types

def extract_wiki_table_data(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            file_content = file.read()

        # Extract headers using regex
        header_pattern = r"\{\|\s*class=\"wikitable.*?\"\s*\n\|(.*?)\n\|\-"
        header_match = re.search(header_pattern, file_content, re.DOTALL)
        if header_match:
            headers = [h.strip().replace('!!', ' ').replace('! align="center"|', '').strip() for h in header_match.group(1).split('!!')]
        else:
            print("No headers found")
            return None

        # Extract rows using a more complex regex
        row_pattern = r"\|\-(?:\s*\|\s*rowspan=\"\d+\"\s*\|)?\s*(\d+)\s*\|\s*\[\[([^\[\]]+)\]\]\s*\|\s*([^\|\n]+)\s*\|\s*''\[\[([^\[\]]+)\]\]''\s*"
        rows = re.findall(row_pattern, file_content, re.DOTALL)
        column_types = detect_column_types(rows)

        # Prepare JSON output structure
        json_output = {
            "header": headers,
            "rows": rows,
            "column_types": column_types,
            "key_column": 0,
            "numeric_columns": [i for i, t in enumerate(column_types) if t == 'numeric'],
            "date_columns": {}
        }

        return json_output

    except Exception as e:
        print(f"Failed to process {file_path}: {str(e)}")
        return None

def save_to_json(data, output_path):
    try:
        with open(output_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        print(f"Data successfully saved to {output_path}")
    except Exception as e:
        print(f"Failed to save data: {str(e)}")

# Specify file paths
files = [
    ("P2/tables_output-instance_1.json", "output_instance_1.json"),
    ("P2/tables_output-instance_2.json", "output_instance_2.json")
]

# Process each file and save the output
for input_path, output_path in files:
    result = extract_wiki_table_data(input_path)
    if result:
        save_to_json(result, output_path)
    else:
        print(f"Failed to process {input_path}")
