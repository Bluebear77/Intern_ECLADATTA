import json
import os

def clean_entry(entry):
    # Remove leading/trailing whitespaces, exclamation marks, and normalize spaces
    return ' '.join(entry.replace('!', '').strip().split())

def process_entries(entries):
    # Process each entry by cleaning and removing empty ones
    return [clean_entry(entry) for entry in entries if clean_entry(entry)]

def check_and_remove_header_row(input_json_file_path, output_json_file_path):
    try:
        # Load the JSON data from file
        with open(input_json_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f"File not found: {input_json_file_path}. Skipping...")
        return  # Exit the function early if file is not found

    # Process each item in the JSON data
    for item in data:
        header = process_entries(item['header'])
        rows = item['rows']
        
        if not rows:
            continue  # If rows are empty, skip to the next item

        # Process the first row to normalize its format for comparison
        first_row_processed = process_entries(rows[0][0].split('!!'))
        
        # Check if the processed first row matches the header
        if first_row_processed == header:
            # Remove the first row if it matches the header
            item['rows'].pop(0)

    # Save the modified data to a new file
    with open(output_json_file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

# Ensure the output directory exists
output_directory = 'P7'
os.makedirs(output_directory, exist_ok=True)

# Iterate over files in the range
for i in range(1, 101):
    input_json_file_path = f'P6/merged_output_{i}.json'
    output_json_file_path = f'P7/output_{i}.json'
    check_and_remove_header_row(input_json_file_path, output_json_file_path)
