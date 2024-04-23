import json
import os
import re


def clean_text(data):
    # Extended regular expression to handle various HTML-like tags and attributes
    patterns = [
        r'!?scope="[^"]*"',
        r'!?scope="?col"?',
        r'rowspan="?[0-9]*"?',
        r'colspan="?[0-9]*"?',
        r'bgcolor="[^"]*"',
        r'style=[^;]*;',
        r'width="[^"]*"',
        r'align="[^"]*"',
        r'align=left\s*',
        r'align="?[^"\s]*"?',
        r'width:\d+%\"[^"]*',
        r'valign="[^"]*"',
        r'"[0-9]+"',
        r'scope="?row[0-9]*"?',
        r'style="[^"]*"',
        r'style=\\"[^"]*\\"',  # Handles escaped quotes within style attributes
        r'background: #[A-Fa-f0-9]{6}',  # Specifically target background color codes in styles
        r'align=center',  # Remove alignment tags that are likely used in table formatting
        r'class="[^"]*"',  # Remove class attributes completely
        r'width=[^ ]*\s*',  # Remove width attributes
        r'width="\d+%"',  # Remove width percentage attributes
        r'\s*\|\|.*?$',  # Clean up trailing table definition artifacts
        r'\"'  # Remove residual double quotes
    ]
    cleaned_data = data
    for pattern in patterns:
        cleaned_data = re.sub(pattern, '', cleaned_data)
    # Further clean up to remove unnecessary white spaces and newlines
    cleaned_data = re.sub(r'\s{2,}', ' ', cleaned_data).strip()
    return cleaned_data


def extract_tables(input_file, output_file):
    # Open and load the JSON data from the input file
    with open(input_file, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    content = data['Content']
    
    # Regular expression to find tables
    tables = re.findall(r'\{\|.*?\|\}', content, re.DOTALL)
    
    # Write the cleaned extracted tables to the output file
    with open(output_file, 'w', encoding='utf-8') as file:
        for table in tables:
            cleaned_table = clean_text(table)
            file.write(cleaned_table + "\n\n")  # Separate tables by two newlines for clarity

# Define the directories
input_dir = "P1"
output_dir = "P2"

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# Iterate over all files in the P1 directory
for filename in os.listdir(input_dir):
    if filename.endswith(".json"):
        input_file = os.path.join(input_dir, filename)
        # Change the output file name to use .txt instead of .json
        output_file = os.path.join(output_dir, "tables_" + os.path.splitext(filename)[0] + ".txt")
        extract_tables(input_file, output_file)
