import os
import csv
import json

def generate_csv():
    # Set the directory where the JSON files are located
    current_directory = os.getcwd()
    
    # CSV file to store the output
    csv_filename = os.path.join(current_directory, 'output.csv')
    
    # Open the CSV file for writing
    with open(csv_filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        # Write the header row
        writer.writerow(['URL', 'File Name without Extension'])
        
        # List all files in the directory
        for filename in os.listdir(current_directory):
            # Check if the file is a JSON file
            if filename.endswith('.json'):
                # Extract the filename without extension
                name_without_extension = os.path.splitext(filename)[0]
                
                # Open and parse the JSON file
                with open(filename, 'r') as json_file:
                    data = json.load(json_file)
                    # Extract the URL from the JSON structure
                    # Assuming the URL is always the first entry in the URL list
                    url = data['url'][0] if 'url' in data and data['url'] else "No URL Found"
                
                # Write the URL and the filename without extension to the CSV
                writer.writerow([url, name_without_extension])

# Run the function to generate the CSV
generate_csv()
