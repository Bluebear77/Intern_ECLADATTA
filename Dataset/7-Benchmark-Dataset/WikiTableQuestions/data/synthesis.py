import csv
import os
import glob
import json

# Define the base directory containing the page subdirectories
base_url_dir = '../url'

# Get all .csv files in the current directory
input_csv_files = glob.glob("*.csv")

# Iterate over each .csv file found
for source_csv_file in input_csv_files:
    # Create the output CSV filename
    output_csv_file = f"complete-{source_csv_file}"

    # Create a list to hold the data for each output file
    output_data = []

    # Read the current input CSV file
    with open(source_csv_file, mode='r', newline='', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        # Add new columns to the output data
        fieldnames = reader.fieldnames + ['table title', 'url']
        output_data.append(fieldnames)

        # Process each row
        for row in reader:
            source_file = row['source file']
            parts = source_file.split('/')
            page_directory = parts[1].replace('csv', 'page')
            json_filename = parts[2].replace('.csv', '.json')
            json_path = os.path.join(base_url_dir, page_directory, json_filename)

            # Read the JSON file
            try:
                with open(json_path, mode='r', encoding='utf-8') as json_file:
                    data = json.load(json_file)
                    table_title = data.get('title', 'N/A')
                    url = data.get('url', 'N/A')
            except FileNotFoundError:
                table_title = 'Not found'
                url = 'Not found'

            # Add the extracted information to the row
            new_row = row.copy()
            new_row['table title'] = table_title
            new_row['url'] = url
            output_data.append([new_row[field] for field in fieldnames])

    # Write the complete output CSV file
    with open(output_csv_file, mode='w', newline='', encoding='utf-8') as outfile:
        writer = csv.writer(outfile)
        writer.writerows(output_data)

    print(f"Output written to {output_csv_file}")
