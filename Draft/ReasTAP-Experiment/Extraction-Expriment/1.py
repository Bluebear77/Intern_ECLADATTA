import json

# Define a list of tuples containing the input files and their corresponding output files
files = [
    ("instance_36.json", "output-36.json"),
    ("instance_99.json", "output-99.json"),
    ("instance_9.json", "output-9.json")
]

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

# Process each file pair
for input_file, output_file in files:
    extract_and_save_data(input_file, output_file)
