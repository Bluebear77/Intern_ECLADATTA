import os
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def read_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def calculate_cosine_similarity(text1, text2):
    vectorizer = TfidfVectorizer().fit_transform([text1, text2])
    vectors = vectorizer.toarray()
    return cosine_similarity(vectors)[0, 1]

def main():
    qas_file_path = './embedding/qas/qas_29/qas_29_table_5.txt'
    text_file_path = './embedding/text/instance_29/section_14.txt'
    
    if os.path.exists(qas_file_path) and os.path.exists(text_file_path):
        qas_text = read_file(qas_file_path)
        text_content = read_file(text_file_path)
        similarity = calculate_cosine_similarity(qas_text, text_content)
        print(f'Cosine Similarity between {qas_file_path} and {text_file_path}: {similarity:.4f}')
    else:
        print('One or both of the files do not exist.')

if __name__ == "__main__":
    main()
