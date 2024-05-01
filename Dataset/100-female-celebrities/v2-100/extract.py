import os
import json

def extract_data(input_path, output_path):
    # Ensure the output directory exists
    if not os.path.exists(os.path.dirname(output_path)):
        os.makedirs(os.path.dirname(output_path))
    
    # Read the input JSON file
    with open(input_path, 'r') as file:
        data = json.load(file)
    
    # Extract required data
    source = data['_source']
    identification = source['identificationMetadata']
    extraction = source['extractionMetadata'][0]
    
    extracted_data = {
        "id": identification["id"],
        "title": identification["title"],
        "url": identification["url"],
        "tableData": extraction["tables"][0]["tableData"]  # Assuming we are interested in the first table
    }
    
    # Write the extracted data to the output JSON file
    with open(output_path, 'w') as file:
        json.dump(extracted_data, file, indent=4)

# Loop through each instance
for i in range(1, 101):
    input_file = f"Raw/instance_{i}.json"
    output_file = f"P1/instance_{i}.json"
    extract_data(input_file, output_file)
