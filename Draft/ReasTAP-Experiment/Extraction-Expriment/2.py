import json
import re

# List of input files and output file paths
files = [
    ("output-36.json", "tables_output-36.json"),
    ("output-99.json", "tables_output-99.json"),
    ("output-9.json", "tables_output-9.json")
]

def extract_tables(input_file, output_file):
    # Open and load the JSON data from the input file
    with open(input_file, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    content = data['Content']
    
    # Regular expression to find tables
    tables = re.findall(r'\{\|.*?\|\}', content, re.DOTALL)
    
    # Write the extracted tables to the output file
    with open(output_file, 'w', encoding='utf-8') as file:
        for table in tables:
            file.write(table + "\n\n")  # Separate tables by two newlines for clarity

# Process each file and extract tables
for input_file, output_file in files:
    extract_tables(input_file, output_file)

# Provide paths to the output files for user download
[file[1] for file in files]
