import os
import json
import glob

def process_json_file(file_path):
    # Get the base file name without extension
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    
    # Create a directory named after the base file name under ./text
    output_dir = os.path.join(os.getcwd(), 'text', base_name)
    os.makedirs(output_dir, exist_ok=True)
    
    # Read the JSON file
    with open(file_path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
    
    extraction_metadata = data["_source"]["extractionMetadata"]
    
    # Iterate over each extraction metadata object
    for metadata in extraction_metadata:
        texts = metadata.get("texts", [])
        
        # Iterate over each section in texts
        for idx, section in enumerate(texts):
            title = section.get('title', 'Untitled')
            value = section.get('value', '')
            
            # Construct the content to be written
            content = f"Title: {title}\n\nValue:\n{value}"
            
            # Define the output file path
            output_file_path = os.path.join(output_dir, f'section_{idx+1}.txt')
            
            # Write the content to the output file
            with open(output_file_path, 'w', encoding='utf-8') as output_file:
                output_file.write(content)

# Get the list of JSON files matching the pattern in the ./input-json directory
json_files = glob.glob('./input-json/instance_*.json')

# Process each JSON file
for json_file in json_files:
    process_json_file(json_file)

print("Processing complete.")
