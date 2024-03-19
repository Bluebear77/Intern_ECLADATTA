import re
import csv

# Initialize a list to hold the names
names = []

# Use regex to find patterns that look like the title within identificationMetadata
# pattern = re.compile(r'"identificationMetadata":\s*{\s*[^}]*"title":\s*"([^"]+)"')

# Define the regex pattern to capture names and first URLs
pattern = re.compile(r'"title":\s*"([^"]+)"[^}]*"url":\s*\[\s*"([^"]+)"')

# Path to the JSON file
file_path = 'part_21.json'

# Open the file and search for the pattern
with open(file_path, 'r', encoding='utf-8') as file:
    content = file.read()
    matches = pattern.findall(content)

    for match in matches:
        names.append(match)

# Path for the output CSV file
output_file_path = '11.csv'

# Save the extracted names to a CSV file
with open(output_file_path, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    for name in names:
        writer.writerow([name])
