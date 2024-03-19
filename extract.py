# You can see the extracted result in total 18293 instances :
# https://docs.google.com/spreadsheets/d/1losvYDlihHk0WSyKhIncAZv-JCjmAFy8XsMeDsICBpc/edit?usp=sharing

import re
import csv
import glob
import os

# Initialize a list to hold the combined extracted data
extracted_data = []

# Get the current working directory
current_directory = os.getcwd()

# Define separate regex patterns for names, URLs, and the first category
pattern_name = re.compile(r'"identificationMetadata":\s*{\s*[^}]*"title":\s*"([^"]+)"')
pattern_urls = re.compile(r'"url":\s*\[\s*"([^"]+)"\s*,\s*"([^"]*)"\s*\]')
pattern_first_category = re.compile(r'"categories":\s*\[\s*"([^"]+)"')

# Loop through each JSON file in the directory
json_files_path = os.path.join(current_directory, '*.json')
for file_path in glob.glob(json_files_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Find all matches for names, URLs, and the first category
    names = pattern_name.findall(content)
    urls = pattern_urls.findall(content)
    categories = pattern_first_category.findall(content)

    # Ensure each part has a match and compile the extracted information
    for i, name in enumerate(names):
        # Check if URLs and categories have a corresponding match; otherwise, use "N/A"
        url1, url2 = urls[i] if i < len(urls) else ("N/A", "N/A")
        category = categories[i] if i < len(categories) else "N/A"
        
        # Append the combined information to the list
        extracted_data.append((name, url1, url2, category))

# Define the output CSV file path, assuming it should be in the same directory as well
output_file_path = os.path.join(current_directory, 'extracted_whole_dataset.csv')

# Write the extracted information to the CSV file
with open(output_file_path, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    # Write the header
    writer.writerow(["Name", "URL1", "URL2", "First Category"])
    # Write the extracted data
    for item in extracted_data:
        writer.writerow(item)
