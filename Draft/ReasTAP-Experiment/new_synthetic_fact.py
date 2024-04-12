from fact_generator.conjunction import generate_conjunction_fact
from fact_generator.counting import generate_counting_fact
from fact_generator.temporal_order import generate_temporal_order_fact
from fact_generator.numerical_comparison import generate_numerical_comparison_fact
from fact_generator.numerical_operation_sum_avg import generate_numerical_operation_sum_avg_fact
from fact_generator.numerical_operation_diff import generate_numerical_operation_diff_fact

from utils.table_wrapper import WikiTable
from utils.multiprocessing_utils import split
from tqdm import tqdm
import multiprocessing as mp
import json
import os
import random
import warnings

warnings.filterwarnings("ignore")
random.seed(233)

fact_func_map = {
    "conjunction": generate_conjunction_fact,
    "counting": generate_counting_fact,
    "temporal_or_numerical_order": generate_temporal_order_fact,
    "numerical_comparison": generate_numerical_comparison_fact,
    "numerical_operation_sum_avg": generate_numerical_operation_sum_avg_fact,
    "numerical_operation_diff": generate_numerical_operation_diff_fact
}

def generate_facts(table, template_data):
    facts = []
    fact_set = set()

    for template_dict in template_data:
        reasoning_type = template_dict["reasoning_type"]
        enable_flag = template_dict["enable"]
        if not enable_flag:
            continue

        for _ in range(template_dict["sample_examples_per_table"]):
            template = random.sample(template_dict["templates"], 1)[0]
            generate_fact_func = fact_func_map[reasoning_type]

            fact = generate_fact_func(table, template["template_str"])
            if fact and fact not in fact_set:
                facts.append({
                    "source": "synthetic_fact",
                    "fact": fact,
                    "reasoning_type": reasoning_type
                })
                fact_set.add(fact)
    return facts

def worker(table_data_chunk, template_dict, q):
    result = []
    for table_data in table_data_chunk:
        table = WikiTable(table_data)
        facts = generate_facts(table, template_dict)
        result.append({"table_data": table_data, "facts": facts})
    q.put(result)

def main():
    template_dict = json.load(open("fact_template.json"))
    table_data_dir = "table_data"
    
    result = []
    files = [f for f in os.listdir(table_data_dir) if f.endswith(".json")]
    for orig_file in tqdm(files):
        orig_file_path = os.path.join(table_data_dir, orig_file)
        
        try:
            with open(orig_file_path, 'r') as file:
                data = json.load(file)
        except json.JSONDecodeError as e:
            print(f"Error reading JSON from {orig_file_path}: {e}")
            continue

        # Set up multiprocessing
        n_processes = mp.cpu_count()
        q = mp.Queue()
        table_chunks = split(data, n_processes)
        processes = [mp.Process(target=worker, args=(table_chunk, template_dict, q)) for table_chunk in table_chunks]

        for p in processes:
            p.start()

        for _ in range(n_processes):
            result.extend(q.get())

        for p in processes:
            p.join()

    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    json.dump(result, open(os.path.join(output_dir, "synthetic_fact_output.json"), "w"), indent=4)
    
    print(f"Generated {len(result)} facts.")

if __name__ == '__main__':
    main()
