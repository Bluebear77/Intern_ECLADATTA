import json
import os
import re

def extract_tables(input_file, output_file):
    # Open and load the JSON data from the input file
    with open(input_file, 'r', encoding='utf-8') as file:
        data = json.load(file)

    content = data['Content']

    # Regular expression to find tables
    # tables = re.findall(r'\{\|.*?\|\}', content, re.DOTALL)
    tables = re.findall(r'(\{\|(?:(?!\{\|).)*?\|\})', content, re.DOTALL)

    # Write the extracted tables to the output file
    with open(output_file, 'w', encoding='utf-8') as file:
        for table in tables:
            file.write(table + "\n\n")  # Separate tables by two newlines for clarity

# Define the directories
input_dir = "P1"
output_dir = "P2"

# Iterate over all files in the P1 directory
for filename in os.listdir(input_dir):
    if filename.endswith(".json"):
        input_file = os.path.join(input_dir, filename)
        # Change the output file name to use .txt instead of .json
        output_file = os.path.join(output_dir, "tables_" + os.path.splitext(filename)[0] + ".txt")
        extract_tables(input_file, output_file)

# Provide paths to the output files for user download
[file.replace("P1", "P2").replace(".json", ".txt") for file in os.listdir("P1") if file.endswith(".json")]
