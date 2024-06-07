import os
import json

def count_tables_in_json_files(directory):
    total_tables = 0
    
    # Iterate over all files in the given directory
    for filename in os.listdir(directory):
        # Check if the file is a .json file
        if filename.endswith('.json'):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r', encoding='utf-8') as file:
                data = json.load(file)
                # Count the number of tables in the current JSON file
                tables_in_file = sum(1 for item in data if 'table' in item)
                print(f"{filename}: {tables_in_file} tables")
                total_tables += tables_in_file
    
    print(f"Total number of tables in all .json files: {total_tables}")

if __name__ == "__main__":
    current_directory = os.getcwd()
    count_tables_in_json_files(current_directory)
