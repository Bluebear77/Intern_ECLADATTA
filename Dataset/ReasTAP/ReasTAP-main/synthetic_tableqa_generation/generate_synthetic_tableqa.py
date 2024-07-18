import os
import random
import json
import warnings
import multiprocessing as mp
from tqdm import tqdm
from nltk.corpus import wordnet
import nltk
from utils.generate_condition import *
from utils.table_wrapper import WikiTable
from utils.multiprocessing_utils import *
from question_generator.conjunction import *
from question_generator.quantifiers import *
from question_generator.temporal_comparison import *
from question_generator.numerical_comparison import *
from question_generator.date_difference import *
from question_generator.counting import *
from question_generator.numerical_operation import *

nltk.download('wordnet')

random.seed(233)

warnings.filterwarnings("ignore")

type_func_map = {
    "conjunction": generate_conjunction_question,
    "quantifiers": generate_quantifier_question,
    "temporal_comparison": generate_temporal_comparison_question,
    "date_difference": generate_date_difference_question,
    "counting": generate_counting_question,
    "numerical_comparison": generate_numerical_comparison_question,
    "numerical_operation": generate_numerical_operation_question
}

def generate_questions(table, template_data, file_name, max_trails=50):
    qas = []
    question_set = set()
    for template_dict in template_data:
        reasoning_type = template_dict["reasoning_type"]
        enable_flag = template_dict["enable"]
        if not enable_flag:
            continue
        for _ in range(template_dict["sample_examples_per_table"]):
            template = random.sample(template_dict["templates"], 1)[0]
            template_type = template["type"]
            generate_question_func = type_func_map[reasoning_type]

            time, question = 0, None
            while question is None and time < max_trails:
                try:
                    question, answer = generate_question_func(table, template["template_str"], template_type)
                except Exception as e:
                    log_error(f"Error generating question for template {template} in file {file_name}: {e}")
                    #log_error(f"Error generating question for template {template} in file {file_name}: {e}")

                    break
                time += 1

            if question is not None and len(answer) > 0 and question not in question_set:
                qas.append({
                    "source": "synthetic_qa",
                    "question": question,
                    "answers": answer,
                    "reasoning_type": reasoning_type
                })
                question_set.add(question)
    return qas

def worker(table_data_chunk, template_dict, file_name, q):
    result = []
    for table_data in table_data_chunk:
        try:
            qas = generate_questions(table_data, template_dict, file_name)
            table_data["qas"] = qas
            result.append(table_data)
        except Exception as e:
            log_error(f"Error processing table {table_data} in file {file_name}: {e}")
            
    q.put(result)

def log_error(message):
    with open("log.txt", "a") as log_file:
        log_file.write(message + "\n")
    # print(message)

def main():
    template_dict = json.load(open("question_template.json"))
    table_data_dir = "../../../subcorpus-100-business-telco-celebrity/telco-100/P5"
    #table_data_dir = "../../../100-female-celebrities/v2-100/P6"
    
    files = [f for f in os.listdir(table_data_dir) if f.endswith(".json")]
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    for orig_file in tqdm(files):
        orig_file_path = os.path.join(table_data_dir, orig_file)
        
        try:
            with open(orig_file_path, 'r') as file:
                data = json.load(file)
        except json.JSONDecodeError as e:
            log_error(f"Error reading JSON from {orig_file_path}: {e}")
            continue

        try:
            # Set up multiprocessing
            n_processes = mp.cpu_count()
            q = mp.Queue()
            table_chunks = split(data, n_processes)
            processes = [mp.Process(target=worker, args=(table_chunk, template_dict, orig_file, q)) for table_chunk in table_chunks]

            for p in processes:
                p.start()

            result = []
            for _ in range(n_processes):
                result.extend(q.get())

            for p in processes:
                p.join()

            output_file_path = os.path.join(output_dir, f"synthetic_qa_output_{orig_file}")
            with open(output_file_path, 'w') as output_file:
                json.dump(result, output_file, indent=4)
            
            print(f"Generated {len(result)} questions for {orig_file}.")
        except Exception as e:
            #log_error(f"Error processing file {orig_file}: {e}")
            log_error(f"Error processing file {orig_file_path}: {e}")


if __name__ == '__main__':
    main()
