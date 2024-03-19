import re
import csv

# Prompt the user to enter the URL
input_url = input("Please enter the URL: ")

# Initialize a list to hold the combined extracted data
extracted_data = []

# Open the JSON file and read its content
file_path = 'whole_v2.json'  # Update this to the correct path
with open(file_path, 'r', encoding='utf-8') as file:
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
    # Directly extract categories without JSON loads, considering the structure of the string
    categories = match.split('", "')
    # Clean up quotes and brackets
    categories = [cat.strip('"') for cat in categories]
    all_categories = ", ".join(categories)
    all_categories_list.append(all_categories)

# Filtering and compiling the information for the matching URL
for i, (name, url_pair) in enumerate(zip(names, urls)):
    url1, url2 = url_pair
    if input_url == url1 or input_url == url2:
        all_categories = all_categories_list[i] if i < len(all_categories_list) else "N/A"
        # Append the combined information to the list
        extracted_data.append([name, url1, url2, all_categories])
        break  # Assuming only one match is needed; remove this if multiple matches should be supported

# Output the result
if extracted_data:
    # Print or save to a CSV file as needed
    print("Name, URL1, URL2, All Categories")
    for data in extracted_data:
        print(", ".join(data))
else:
    print("No match found for the given URL.")

