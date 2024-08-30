import json
import os

# Function to split the data into chunks
def split_data(data, chunk_size):
    for i in range(0, len(data), chunk_size):
        yield data[i:i + chunk_size]

# Path to the input JSON file in the parent directory
input_file_path = os.path.join('.', 'filtered_qtsumm.json')

# Load the input JSON file
with open(input_file_path, 'r') as file:
    data = json.load(file)

# Define the chunk size
chunk_size = 10

# Split the data into smaller chunks
chunks = list(split_data(data, chunk_size))

# Directory to save the chunks
output_dir = 'chunks'
os.makedirs(output_dir, exist_ok=True)

# Save each chunk as a separate JSON file
for i, chunk in enumerate(chunks):
    chunk_filename = os.path.join(output_dir, f'v1_chunk_{i + 1}.json')
    with open(chunk_filename, 'w') as chunk_file:
        json.dump(chunk, chunk_file, indent=4)

    print(f'Saved {chunk_filename}')
