import random
import json
import os
from utils.generate_condition import generate_condition_for_column
from utils.table_wrapper import WikiTable
from tqdm import tqdm
import warnings
import multiprocessing as mp
warnings.filterwarnings("ignore")

def generate_conjunction_fact(table_data, fact_template):
    '''
    "fact_template": "The [target_col] that have [condition] are [executed_results]."
    '''
    table = WikiTable(table_data)
    
    # Select target column at random for simplicity, could be based on specific logic
    target_col_idx = random.choice(range(len(table.header)))
    target_col_name = table.header[target_col_idx]

    # Generate a condition for a random column, which could also be based on specific logic
    source_col_idx, source_col_data, condition = generate_condition_for_column(table)
    if condition is None or source_col_idx == target_col_idx: # Ensure target and condition cols are not the same
        return None, None

    # Constructing the fact based on the template
    fact = fact_template.replace("[target_col]", target_col_name).replace("[condition]", condition)

    # Assuming executed_results requires fetching specific row data, which is skipped for simplicity
    executed_results = "specific data based on the condition"  # Placeholder

    fact = fact.replace("[executed_results]", executed_results)
    
    return fact

if __name__ == "__main__":
    table_data_path = "path/to/table_data.json"  # Adjust as necessary
    table_data = json.loads(open(table_data_path, 'r').read())

    fact_template = "The [target_col] that have [condition] are [executed_results]."
    for table in tqdm(table_data):
        generated_fact = generate_conjunction_fact(table, fact_template)
        if generated_fact:
            print(f"Generated Fact: {generated_fact}")
