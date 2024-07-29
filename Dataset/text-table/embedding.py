import os
from sentence_transformers import SentenceTransformer
import numpy as np
from tqdm import tqdm

# Load the pre-trained model

model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-mpnet-base-v2')

#model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')

# Define input and output directory pairs
dirs = [
    #{'input': './qas', 'output': './embedding/qas'},
    {'input': './text', 'output': './embedding/text'}
]

# Process each directory pair
for dir_pair in dirs:
    input_dir = dir_pair['input']
    output_dir = dir_pair['output']
    
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Get the list of all files to process for the progress bar
    all_files = []
    for root, _, files in os.walk(input_dir):
        for file in files:
            if file.endswith('.txt'):
                all_files.append(os.path.join(root, file))

    # Iterate through all subdirectories and files in the input directory with progress bar
    for file_path in tqdm(all_files, desc=f"Processing {input_dir}", unit="file"):
        # Read the file content
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read().splitlines()

        # Encode the content using the model
        embeddings = model.encode(content)

        # Construct the corresponding output file path
        relative_path = os.path.relpath(file_path, input_dir)
        output_file_path = os.path.join(output_dir, relative_path)

        # Ensure the output subdirectory exists
        os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

        # Save the embeddings to the output file
        np.savetxt(output_file_path, embeddings)

print("Embedding generation completed.")
