import os
import glob
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from tqdm import tqdm

def read_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def calculate_cosine_similarity(text1, text2):
    vector1 = np.array([float(num) for num in text1.split()])
    vector2 = np.array([float(num) for num in text2.split()])
    return cosine_similarity([vector1], [vector2])[0][0]

def process_directories(qas_root, text_root, output_root):
    qas_dirs = glob.glob(os.path.join(qas_root, 'qas_*'))
    for qas_dir in tqdm(qas_dirs, desc="Processing QAS Directories"):
        qas_index = os.path.basename(qas_dir).split('_')[1]
        text_dir = os.path.join(text_root, f'instance_{qas_index}')
        if os.path.exists(text_dir):
            qas_files = glob.glob(os.path.join(qas_dir, '*.txt'))
            text_files = glob.glob(os.path.join(text_dir, '*.txt'))
            output_data = []
            for qas_file in tqdm(qas_files, desc=f"Processing files in {qas_dir}", leave=False):
                qas_text = read_file(qas_file)
                qas_filename = os.path.basename(qas_file)
                for text_file in text_files:
                    text_content = read_file(text_file)
                    similarity = calculate_cosine_similarity(qas_text, text_content)
                    text_filename = os.path.basename(text_file)
                    output_data.append([similarity, qas_filename, text_filename])
            
            if output_data:
                output_subdir = os.path.join(output_root, f'qas_{qas_index}')
                os.makedirs(output_subdir, exist_ok=True)
                output_file_path = os.path.join(output_subdir, 'cosine_similarity.csv')
                df = pd.DataFrame(output_data, columns=['Similarity', 'QAS_File', 'Text_File'])
                df.to_csv(output_file_path, index=False)

if __name__ == "__main__":
    qas_root = './embedding/qas'
    text_root = './embedding/text'
    output_root = './embedding/output'

    process_directories(qas_root, text_root, output_root)

'''
import os
import glob
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from tqdm import tqdm

def read_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def pad_vectors(vector1, vector2):
    max_len = max(len(vector1), len(vector2))
    padded_vector1 = np.pad(vector1, (0, max_len - len(vector1)), 'constant')
    padded_vector2 = np.pad(vector2, (0, max_len - len(vector2)), 'constant')
    return padded_vector1, padded_vector2

def calculate_cosine_similarity(text1, text2):
    vector1 = np.array([float(num) for num in text1.split()])
    vector2 = np.array([float(num) for num in text2.split()])
    padded_vector1, padded_vector2 = pad_vectors(vector1, vector2)
    return cosine_similarity([padded_vector1], [padded_vector2])[0][0]

def process_directories(qas_root, text_root, output_root):
    qas_dirs = glob.glob(os.path.join(qas_root, 'qas_*'))
    for qas_dir in tqdm(qas_dirs, desc="Processing QAS Directories"):
        qas_index = os.path.basename(qas_dir).split('_')[1]
        text_dir = os.path.join(text_root, f'instance_{qas_index}')
        if os.path.exists(text_dir):
            qas_files = glob.glob(os.path.join(qas_dir, '*.txt'))
            text_files = glob.glob(os.path.join(text_dir, '*.txt'))
            output_data = []
            for qas_file in tqdm(qas_files, desc=f"Processing files in {qas_dir}", leave=False):
                qas_text = read_file(qas_file)
                qas_filename = os.path.basename(qas_file)
                for text_file in text_files:
                    text_content = read_file(text_file)
                    similarity = calculate_cosine_similarity(qas_text, text_content)
                    text_filename = os.path.basename(text_file)
                    output_data.append([similarity, qas_filename, text_filename])
            
            if output_data:
                output_subdir = os.path.join(output_root, f'qas_{qas_index}')
                os.makedirs(output_subdir, exist_ok=True)
                output_file_path = os.path.join(output_subdir, 'cosine_similarity.csv')
                df = pd.DataFrame(output_data, columns=['Similarity', 'QAS_File', 'Text_File'])
                df.to_csv(output_file_path, index=False)

if __name__ == "__main__":
    qas_root = './embedding/qas'
    text_root = './embedding/text'
    output_root = './embedding/output/cosine'

    process_directories(qas_root, text_root, output_root)
'''