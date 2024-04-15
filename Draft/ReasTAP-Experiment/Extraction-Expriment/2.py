import json
import re

def convert_json(input_file_path, output_file_path):
    # Read the input JSON file
    with open(input_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    # Concatenate the table content from the array of arrays of strings
    table_data = ''.join([''.join(sublist) for sublist in data['table']])
    
    # Define regex patterns to extract table headers and row data
    #header_pattern = r'!\s*(?:width=\d+%|[^|]*?)\|\s*([^\n|]+)'
    header_pattern = r'!\s*(?:width=\d+%|[^|]*?)\|\s*([^\|]+?)(?=\n!|\n\||$)'
    

    #r'!\s*width=\d+%\s*\|\s*([^|]+)\n'  # Adjusted to correctly capture header names
    row_pattern = r'\|\s*align="center"[^|]+\|\s*([^|]+)\s*\|'
    
    # Extract headers
    headers = re.findall(header_pattern, table_data)
    
    # Initialize the rows list
    rows = []
    
    # Extract rows data
    split_rows = table_data.split("|-")[1:]  # Skip the header row part
    for row in split_rows:
        extracted_row = re.findall(row_pattern, row)
        if extracted_row:
            # Clean up HTML tags and extra spaces
            cleaned_row = [re.sub(r'<[^>]+>', '', text).strip() for text in extracted_row]
            rows.append(cleaned_row)
    
    # Define the output structure similar to test-table_data.json
    output_data = {
        "id": data.get("id", ""),
        "title": data.get("title", ""),
        "url": data.get("url", []),
        "header": headers,
        "rows": rows,
        "column_types": ["string"] * len(headers),  # Assuming all columns are of type string for simplicity
        "key_column": 0,  # Assuming the first column is the key column
        "numeric_columns": [],
        "date_columns": {}
    }
    
    # Write the transformed data to the output JSON file
    with open(output_file_path, 'w', encoding='utf-8') as file:
        json.dump(output_data, file, indent=4, ensure_ascii=False)

# Usage
input_file_path = 'output.json_table_1.json'
output_file_path = 'formatted_output.json'
convert_json(input_file_path, output_file_path)



