import csv
import os
import glob
import json

# Define the base directory containing the page subdirectories
base_url_dir = '../WikiTableQuestions/url'

# Get all .json files in the current directory
input_json_files = glob.glob("*.json")

# Iterate over each .json file found
for json_file in input_json_files:
    # Create the output CSV filename
    output_csv_file = f"complete-{os.path.splitext(json_file)[0]}.csv"

    # Create a list to hold the data for each output file
    output_data = []
    fieldnames = ['id', 'source file', 'table title', 'url']
    output_data.append(fieldnames)

    # Read the current input JSON file
    with open(json_file, mode='r', encoding='utf-8') as file:
        data = json.load(file)
        for item_key in data:
            item = data[item_key]
            table_info = item.get('table', {})
            id_ = item.get('id', 'N/A')
            source_file = table_info.get('name', 'N/A')

            # Form the path to the JSON file containing the table title and URL
            parts = source_file.split('/')
            if len(parts) == 3:
                page_directory = parts[1].replace('csv', 'page')
                json_filename = parts[2].replace('.tsv', '.json')
                json_path = os.path.join(base_url_dir, page_directory, json_filename)

                # Read the JSON file
                try:
                    with open(json_path, mode='r', encoding='utf-8') as json_file:
                        page_data = json.load(json_file)
                        table_title = page_data.get('title', 'N/A')
                        url = page_data.get('url', 'N/A')
                except FileNotFoundError:
                    table_title = 'Not found'
                    url = 'Not found'

                # Add the extracted information to the output data list
                output_data.append([id_, source_file, table_title, url])

    # Write the complete output CSV file
    with open(output_csv_file, mode='w', newline='', encoding='utf-8') as outfile:
        writer = csv.writer(outfile)
        writer.writerows(output_data)

    print(f"Output written to {output_csv_file}")
