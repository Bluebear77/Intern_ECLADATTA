import os
import re
import csv

def find_files_without_tables_regex(input_directory, output_csv):
    # Regex pattern to find "nbTables": <number>
    regex = re.compile(r'"nbTables":\s*(\d+)')

    # List to store the names of files without tables
    files_without_tables = []
    
    # Walk through all files in the input directory
    for root, dirs, files in os.walk(input_directory):
        for file in files:
            if file.endswith('.json'):  # Check only json files
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        contents = f.read()
                        # Use regex to find 'nbTables'
                        match = regex.search(contents)
                        if match and int(match.group(1)) == 0:
                            files_without_tables.append(file)
                except Exception as e:
                    print(f"Error processing {file}: {e}")

    # Print the number of files found without tables
    print(f"Number of files without tables: {len(files_without_tables)}")

    # Write the list of files without tables to a CSV file
    with open(output_csv, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Filename'])
        for file in files_without_tables:
            writer.writerow([file])

    # Print a message after successfully generating the CSV
    print(f"Output file '{output_csv}' has been successfully generated with the list of files without tables.")

# Usage:
input_directory = './Raw'  # Set your input directory path
output_csv = 'files-with-no-table.csv'  # Set your output CSV file path

# Function call
find_files_without_tables_regex(input_directory, output_csv)
