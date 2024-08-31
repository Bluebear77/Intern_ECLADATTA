import os
import json
from glob import glob
import re
import nltk
from nltk.corpus import stopwords

# Download necessary NLTK data
nltk.download('punkt')
nltk.download('stopwords')

# Define the function to clean text
def clean_text(dirty_text, language='english'):
    # Tokenize words
    words = nltk.word_tokenize(dirty_text, language)

    # Remove punctuation
    words = [re.sub(r'[^\w\s]', '', word) for word in words]
    # Convert to lowercase
    words = [word.lower() for word in words]

    # Remove stopwords
    stop_words = set(stopwords.words(language))
    words = [word for word in words if not word in stop_words]

    # Join words back into a string
    cleaned_text = ' '.join(words)

    # Remove newlines
    cleaned_text = cleaned_text.replace('\n', ' ')

    
    # Return the cleaned text
    return cleaned_text

def process_qas(qas):
    """
    Convert list of QA dictionaries to a formatted string and clean the text.
    """
    output = []
    for qa in qas:
        question = clean_text(qa['question'])
        answers = "".join([clean_text(answer) for answer in qa['answers']])
        output.append(f"Question: {question}Answers:{answers}")
    return "".join(output)

def main():
    # Get list of JSON files following the specified pattern

    #  json_files = glob('../ReasTAP/ReasTAP-main/synthetic_tableqa_generation/output-celebrity/synthetic_qa_output_instance_*_v6.json')
    # json_files = glob('../ReasTAP/ReasTAP-main/synthetic_tableqa_generation/output-business/synthetic_qa_output_instance_*_v5.json')
    # json_files = glob('./fr-multilingual-mpnet-base-v2/5-sample/input-qas/synthetic_qa_output_instance_*_v6.json')
    json_files = glob('./all-mpnet-base-v2/input-qas/synthetic_qa_output_instance_*_v5.json')

    for json_file in json_files:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        # Extract instance index from filename
        instance_index = re.search(r'synthetic_qa_output_instance_(\d+)_v5\.json', json_file).group(1)
        output_dir = f"./qas/qas_{instance_index}"
        
        # Create directory if it doesn't exist
        if not os.path.exists(output_dir):
            print(f"Creating directory: {output_dir}")
            os.makedirs(output_dir, exist_ok=True)
        
        for table_index, table in enumerate(data):
            table_qas = table.get('qas', [])
            if table_qas:
                output_file = os.path.join(output_dir, f"qas_{instance_index}_table_{table_index + 1}.txt")
                print(f"Writing to file: {output_file}")
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(process_qas(table_qas))

if __name__ == "__main__":
    main()
