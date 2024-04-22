import json
import re
import os

def clean_text(data):
    # Extended regular expression to handle various HTML-like tags and attributes
    patterns = [
        r'!?scope="[^"]*"',
        r'rowspan=?[0-9]*',
        r'colspan=?[0-9]*',
        r'bgcolor="[^"]*"',
        r'style=[^;]*;',
        r'width="[^"]*"',
        r'align="[^"]*"',
        r'valign="[^"]*"',
    ]
    cleaned_data = data
    for pattern in patterns:
        cleaned_data = re.sub(pattern, '', cleaned_data)

    cleaned_data = re.sub(r'\s+', ' ', cleaned_data).strip()  # Normalize spaces
    cleaned_data = cleaned_data.replace("''", "'")  # Fix doubled single quotes
    return cleaned_data

def process_file(input_path, output_path):
    # Check if file exists before trying to open it
    if not os.path.exists(input_path):
        print(f"Skipping missing file: {input_path}")
        return

    # Load JSON data from file
    with open(input_path, 'r', encoding='utf-8') as file:
        json_data = json.load(file)

    # Clean the JSON data
    for entry in json_data:
        entry['header'] = [clean_text(header) for header in entry['header']]
        for row in entry['rows']:
            for i in range(len(row)):
                row[i] = clean_text(row[i])

    # Save cleaned JSON data to a new file
    with open(output_path, 'w', encoding='utf-8') as file:
        json.dump(json_data, file, indent=4, ensure_ascii=False)

# Usage
for i in range(1, 101):  # Assumes files are numbered from 1 to 100
    input_path = f'P3/output_instance_{i}.json'
    output_path = f'P4/cleaned_output_instance_{i}.json'
    process_file(input_path, output_path)
