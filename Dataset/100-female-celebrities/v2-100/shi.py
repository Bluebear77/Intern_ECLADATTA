
import os
import json
import csv

# Define the directory containing the raw files
raw_dir = './Raw'

# Initialize the sets and lists to store data
type_set = set()
b_list = []

# Function to extract typing labels
def extract_typing_labels(tech_result):
    global type_set
    has_primitive_typing = 'F'
    for key, value in tech_result.items():
        if isinstance(value, dict):
            preprocessed = value.get('preprocessed', {})
            if 'primitiveTyping' in preprocessed:
                has_primitive_typing = 'T'
                primitive_typing = preprocessed['primitiveTyping']
                for pt_item in primitive_typing:
                    typing = pt_item.get('typing', [])
                    for t in typing:
                        type_set.add(t.get('typingLabel', 'UNKNOWN'))
    return has_primitive_typing

# Iterate over each file in the raw directory
for filename in os.listdir(raw_dir):
    if filename.endswith('.json'):  # Ensure we're only processing JSON files
        file_path = os.path.join(raw_dir, filename)
        with open(file_path, 'r') as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError as e:
                print(f"JSONDecodeError: {e} in file {filename}")
                continue

        # Initialize the boolean for primitiveTyping presence
        has_primitive_typing = 'F'

        # Traverse the nested structure to find the required sections
        try:
            # Navigate to preprocessingMetadata if it exists
            preprocessing_metadata = data['_source'].get('preprocessingMetadata', [])
            for item in preprocessing_metadata:
                technology_results = item.get('technologyResults', [])
                for tech_result in technology_results:
                    # Check if tech_result is a dictionary
                    if isinstance(tech_result, dict):
                        has_primitive_typing = extract_typing_labels(tech_result)
        except KeyError as e:
            print(f"KeyError: {e} in file {filename}")
            continue

        # Append the result for the current file to b_list
        b_list.append([filename, has_primitive_typing])

# Write the type.csv file
with open('type.csv', 'w', newline='') as type_file:
    writer = csv.writer(type_file)
    for type_label in sorted(type_set):
        writer.writerow([type_label])

# Write the b.csv file
with open('b.csv', 'w', newline='') as b_file:
    writer = csv.writer(b_file)
    writer.writerow(['filename', 'primitiveTyping'])  # Write the header
    writer.writerows(b_list)

print("Files generated: type.csv and b.csv")
