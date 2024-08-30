import json

def clean_json(file_path):
    # Read the JSON data from the input file
    with open(file_path, 'r') as file:
        data = json.load(file)

    # Process each dictionary in the array
    for item in data:
        # Filter out empty strings from the header
        filtered_header = [header_item for header_item in item["header"] if header_item]
        
        # Adjust each row to match the new header length
        filtered_rows = [row[:len(filtered_header)] for row in item["rows"]]
        
        # Update the item with cleaned data
        item["header"] = filtered_header
        item["rows"] = filtered_rows
    
    return data

def save_json(data, output_path):
    # Write the updated JSON data to the output file
    with open(output_path, 'w') as file:
        json.dump(data, file, indent=4)

# File paths
input_path = 'P7/output_2.json'
output_path = 'P8/output_2.json'

# Process the data
updated_data = clean_json(input_path)

# Save the cleaned data to a new file
save_json(updated_data, output_path)
