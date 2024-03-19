import re
import csv

# Initialize lists to hold the extracted data
extracted_data = []

# Define the regex pattern to capture names, first URLs, and adjust for first categories
pattern = re.compile(r'"title":\s*"([^"]+)"[^}]*"url":\s*\[\s*"([^"]+)"', re.DOTALL)
pattern_first_category = re.compile(r'"descriptionMetadata":\s*{[^}]*"categories":\s*\[\s*"(.*?)"', re.DOTALL)

# Path to the JSON file
file_path = 'part_21.json'

# Open the file and search for the patterns
with open(file_path, 'r', encoding='utf-8') as file:
    content = file.read()
    matches = pattern.findall(content)
    categories_matches = pattern_first_category.findall(content)
    
    # Ensure we have matched categories for each entry found by the first pattern
    for i, match in enumerate(matches):
        # If there are not enough category matches, append "N/A" for missing categories
        category = categories_matches[i] if i < len(categories_matches) else "N/A"
        extracted_data.append((match[0], match[1], category))

# Path for the output CSV file
output_file_path = '11.csv'

# Save the extracted names, URLs, and first categories to a CSV file
with open(output_file_path, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Name", "First URL", "First Category in 'descriptionMetadata'"])  # Write the header
    for data in extracted_data:
        writer.writerow(data)
