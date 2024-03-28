import json
import os

def split_json_file(file_path, output_folder, num_files=20):
    # Create the output directory if it does not exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Load the data from the large JSON file
    data = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            try:
                data.append(json.loads(line))
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON from line: {e}")
    
    # Continue as before if data length is sufficient
    if not data:
        print("No data loaded.")
        return

    # Calculate the number of elements per file
    total_length = len(data)
    chunk_size = total_length // num_files
    if total_length % num_files:
        num_files += 1  # If there's a remainder, we need one more file

    # Split and save the data
    for i in range(num_files):
        start_index = i * chunk_size
        end_index = start_index + chunk_size if i < num_files - 1 else total_length
        chunk_data = data[start_index:end_index]

        chunk_file_name = os.path.join(output_folder, f'part_{i+1}.json')
        with open(chunk_file_name, 'w', encoding='utf-8') as chunk_file:
            for item in chunk_data:
                json.dump(item, chunk_file, ensure_ascii=False, indent=4)
                chunk_file.write('\n')  # Write each JSON object on a new line
    
    print(f"Data split into {num_files} files and saved in {output_folder}")

# Specify the path to your large JSON file and the desired output folder
file_path = 'whole_v2.json'
output_folder = 'split_json'

# Call the function
split_json_file(file_path, output_folder)

