import os
import json
from fuzzywuzzy import fuzz

# Base directory containing the page folders
base_dir = '.'
page_dirs = ['200-page', '201-page', '202-page', '203-page', '204-page']

# Threshold for similarity matching
SIMILARITY_THRESHOLD = 80

def clean_input(input_str):
    """Remove dashes from the input string."""
    return input_str.replace('-', '')

def is_similar(target_hashcode, json_hashcode):
    """Check similarity between target and json hashcodes using fuzzy matching."""
    similarity = fuzz.ratio(target_hashcode, json_hashcode)
    return similarity >= SIMILARITY_THRESHOLD

def find_file_by_hashcode(target_hashcode):
    # Clean the input hashcode
    target_hashcode = clean_input(target_hashcode)

    # Iterate through each page directory
    for page_dir in page_dirs:
        full_page_dir_path = os.path.join(base_dir, page_dir)
        
        # List all JSON files in the current directory
        for root, _, files in os.walk(full_page_dir_path):
            for file in files:
                if file.endswith('.json'):
                    json_path = os.path.join(root, file)

                    # Open and read the JSON file
                    with open(json_path, mode='r', encoding='utf-8') as json_file:
                        try:
                            data = json.load(json_file)
                            json_hashcode = data.get('hashcode')
                            if json_hashcode and is_similar(target_hashcode, json_hashcode):
                                return json_path
                        except json.JSONDecodeError:
                            print(f"Error reading {json_path}")
    # If no file is found with a similar hash code
    return None

# Example usage:
target_hashcode = "a560358f-7a28-4652-8cb7-43e1e6273849"
file_path = find_file_by_hashcode(target_hashcode)

if file_path:
    print(f"JSON file found at: {file_path}")
else:
    print(f"No JSON file found with a similar hash code to: {target_hashcode}")
