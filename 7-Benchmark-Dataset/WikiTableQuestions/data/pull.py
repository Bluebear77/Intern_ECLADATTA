import os
import re
import csv

# Function to extract ID and source file information
def parse_examples(file_path):
    pattern = re.compile(r'\(id ([^\)]+)\).*?graph tables.TableKnowledgeGraph (csv/[^\)]+)\)')
    results = []
    with open(file_path, 'r') as file:
        content = file.read()
        results = pattern.findall(content)
    return results

# Function to write extracted data to a CSV file
def write_to_csv(data, output_file):
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['id', 'source file'])
        writer.writerows(data)

# Function to process each .examples file in the current directory
def process_files_in_directory():
    current_dir = os.getcwd()
    for file_name in os.listdir(current_dir):
        if file_name.endswith('.examples'):
            base_name = os.path.splitext(file_name)[0]
            csv_file_name = f"{base_name}.csv"
            examples_data = parse_examples(file_name)
            write_to_csv(examples_data, csv_file_name)
            print(f"Generated CSV file: {csv_file_name}")

# Execute the processing function
process_files_in_directory()
