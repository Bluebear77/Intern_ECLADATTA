from utils.generate_condition import *
from utils.table_wrapper import WikiTable
from utils.multiprocessing_utils import *

from tqdm import tqdm
import warnings
import multiprocessing as mp
import json
import os
import random

from question_generator.conjunction import *
from question_generator.quantifiers import *
from question_generator.temporal_comparison import *
from question_generator.numerical_comparison import *
from question_generator.date_difference import *
from question_generator.counting import *
from question_generator.numerical_operation import *

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

def generate_questions(table, template_data, max_trails=50):
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
            while question == None and time < max_trails:
                try:
                    question, answer = generate_question_func(table, template["template_str"], template_type)
                except ValueError as e:
                    return []  # Return an empty list if there's an error
                time += 1
                
            if question != None and len(answer) > 0 and question not in question_set:
                qas.append({
                    "source": "synthetic_qa",
                    "question": question,
                    "answers": answer,
                    "reasoning_type": reasoning_type
                })
                question_set.add(question)
    return qas

def worker(table_data_chunk, template_dict, q):
    result = []
    for table_data in table_data_chunk:
        qas = generate_questions(table_data, template_dict)
        table_data["qas"] = qas
        result.append(table_data)
    q.put(result)

def main():
    template_dict = json.load(open("question_template.json"))
    table_data_dir = "table_data"
    output_dir = "output"
    log_file = os.path.join(output_dir, "log.md")
    os.makedirs(output_dir, exist_ok=True)
    log_entries = []

    for orig_file in tqdm(os.listdir(table_data_dir)):
        if not orig_file.endswith(".json"):
            continue
        orig_file_path = os.path.join(table_data_dir, orig_file)
        try:
            data = json.load(open(orig_file_path))
            n_processes = mp.cpu_count()
            q = mp.Queue()
            table_chunks = split(data, n_processes)
            processes = [mp.Process(target=worker, args=(table_chunk, template_dict, q)) for table_chunk in table_chunks]

            for p in processes:
                p.start()

            all_results = []
            for _ in range(n_processes):
                all_results.extend(q.get())

            for p in processes:
                p.join()

            output_path = os.path.join(output_dir, f"{orig_file.split('.')[0]}_output.json")
            json.dump(all_results, open(output_path, "w"), indent=4)
        except Exception as e:
            log_entries.append(f"Error processing {orig_file}: {str(e)}\n")

    with open(log_file, "w") as lf:
        for entry in log_entries:
            lf.write(entry)

if __name__ == '__main__':
    main()
