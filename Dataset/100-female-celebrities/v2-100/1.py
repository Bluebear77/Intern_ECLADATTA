import json
import os

def extract_and_save_data(input_file, output_file):
    # Open and load the JSON data from the input file
    with open(input_file, 'r') as file:
        data = json.load(file)
    
    # Extract the required information
    id = data['_source']['identificationMetadata']['id']
    title = data['_source']['identificationMetadata']['title']
    urls = data['_source']['identificationMetadata']['url']
    content = data['_source']['contentMetadata']['content']

    # Prepare the extracted data as a dictionary
    extracted_data = {
        "ID": id,
        "Title": title,
        "URLs": urls,
        "Content": content
    }

    # Save extracted data to the specified output file
    with open(output_file, 'w') as output_file:
        json.dump(extracted_data, output_file, indent=4)

# Define the directories
raw_dir = "Raw"
output_dir = "P1"

# Iterate over all files in the Raw directory
for filename in os.listdir(raw_dir):
    if filename.endswith(".json"):
        input_file = os.path.join(raw_dir, filename)
        output_file = os.path.join(output_dir, "output-" + filename)
        extract_and_save_data(input_file, output_file)
