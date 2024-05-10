import os
import json
import csv

# Define the base directory containing the subdirectories
base_directory = '.'

# List the subdirectories containing JSON files
subdirectories = ['200-page', '201-page', '202-page', '203-page', '204-page']

# Process each subdirectory
for subdirectory in subdirectories:
    # Construct the full path to the subdirectory
    subdirectory_path = os.path.join(base_directory, subdirectory)
    
    # Initialize an empty list to hold the extracted URLs
    extracted_data = []

    # Iterate through each file in the subdirectory
    for file_name in os.listdir(subdirectory_path):
        if file_name.endswith('.json'):
            file_path = os.path.join(subdirectory_path, file_name)
            # Read and parse each JSON file
            with open(file_path, 'r', encoding='utf-8') as json_file:
                data = json.load(json_file)
                # Extract the URL and store it in the list
                extracted_data.append([data['url']])

    # Write the extracted URLs to a CSV file in the same directory
    csv_output_path = os.path.join(base_directory, f'{subdirectory}.csv')
    with open(csv_output_path, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        # Write the header row
        writer.writerow(['URL'])
        # Write the extracted URLs
        writer.writerows(extracted_data)

    print(f'Successfully extracted URLs to {csv_output_path}')
