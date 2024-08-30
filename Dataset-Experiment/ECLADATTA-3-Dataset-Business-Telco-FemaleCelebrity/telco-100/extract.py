import os
import json

def extract_data(input_path, output_path):
    # Ensure the output directory exists
    if not os.path.exists(os.path.dirname(output_path)):
        os.makedirs(os.path.dirname(output_path))
    
    # Read the input JSON file with explicit UTF-8 encoding
    with open(input_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    # Extract required data
    source = data['_source']
    identification = source['identificationMetadata']
    extraction_metadata = source['extractionMetadata'][0]  # Assuming we are only interested in the first extractionMetadata block

    # Collect all tableData from each table
    table_data_list = [table['tableData'] for table in extraction_metadata['tables'] if 'tableData' in table]
    
    extracted_data = {
        "id": identification["id"],
        "title": identification["title"],
        "url": identification["url"],
        "tableData": table_data_list
    }
    
    # Write the extracted data to the output JSON file with UTF-8 encoding
    with open(output_path, 'w', encoding='utf-8') as file:
        json.dump(extracted_data, file, indent=4, ensure_ascii=False)



def main():
  
    # Loop through possible instance numbers
    for i in range(1, 102):  # Assuming the numbering starts from 1 and goes up to 101
        input_file = f"Complete/instance_{i}.json"
        output_file = f"P1/instance_{i}.json"
        
        # Check if the input file exists before processing
        if os.path.exists(input_file):
            extract_data(input_file, output_file)
        else:
            print(f"File not found: {input_file}")

if __name__ == "__main__":
    main()
