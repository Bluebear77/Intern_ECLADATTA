import os
import json
from glob import glob

def process_qas(qas):
    """
    Convert list of QA dictionaries to a formatted string.
    """
    output = []
    for qa in qas:
        question = qa['question']
        answers = "\n".join(qa['answers'])
        output.append(f"Question: {question}\nAnswers:\n{answers}\n")
    return "\n".join(output)

def main():
    # Get list of JSON files following the specified pattern
    json_files = glob('synthetic_qa_output_instance_*_v6.json')
    
    for json_file in json_files:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        # Extract instance index from filename
        instance_index = json_file.split('_')[4]
        output_dir = f"./qas/qas_{instance_index}"
        
        # Create directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        for table_index, table in enumerate(data):
            table_qas = table.get('qas', [])
            if table_qas:
                output_file = os.path.join(output_dir, f"qas_{instance_index}_table_{table_index + 1}.txt")
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(process_qas(table_qas))
                    
if __name__ == "__main__":
    main()
