import re
import csv

# Function to read URLs from a CSV file and return them as a list
def read_urls_from_csv(csv_file_path):
    with open(csv_file_path, mode='r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        return [row[0] for row in reader]

# Function to write the extracted data to a CSV file
def write_to_csv(output_file_path, data):
    with open(output_file_path, mode='w', encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Name", "URLs", "All Categories"])
        writer.writerows(data)

# File paths
input_csv_path = '3unique_urls.csv'  # Update this to the correct path of your input CSV
output_csv_path = 'v2-extracted_data.csv'  # Path for the output CSV file
json_file_path = 'whole_v2.json'  # Update this to the correct path of your JSON file

# Read URLs from the CSV file
input_urls = read_urls_from_csv(input_csv_path)

# Initialize a list to hold the combined extracted data
extracted_data = []

# Open the JSON file and read its content
with open(json_file_path, 'r', encoding='utf-8') as file:
    content = file.read()

# Define regex patterns for names, URLs, and all categories
pattern_name = re.compile(r'"identificationMetadata":\s*{\s*[^}]*"title":\s*"([^"]+)"')
pattern_urls = re.compile(r'"url":\s*\[\s*"([^"]+)"\s*,\s*"([^"]*)"\s*\]')
pattern_all_categories = re.compile(r'"categories":\s*\[(.*?)\]', re.DOTALL)

# Find all matches for names, URLs, and all categories
names = pattern_name.findall(content)
urls = pattern_urls.findall(content)
matches_categories = pattern_all_categories.findall(content)

# Process all categories to extract them correctly
all_categories_list = []
for match in matches_categories:
    categories = match.split('", "')
    categories = [cat.strip('"[]') for cat in categories]  # Clean up quotes and brackets
    all_categories = ", ".join(categories)
    all_categories_list.append(all_categories)

# Compile the information for each URL found in the input CSV
for url in input_urls:
    for i, url_pair in enumerate(urls):
        if url in url_pair:
            name = names[i] if i < len(names) else "N/A"
            all_categories = all_categories_list[i] if i < len(all_categories_list) else "N/A"
            extracted_data.append([name, url, all_categories])

# Write the extracted data to the output CSV file
write_to_csv(output_csv_path, extracted_data)

print(f"Extraction completed. Data saved to {output_csv_path}.")
