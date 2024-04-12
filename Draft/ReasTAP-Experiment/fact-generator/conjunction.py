import random
import json
import os

from utils.generate_condition import generate_condition
from utils.table_wrapper import WikiTable
from tqdm import tqdm
import warnings
import multiprocessing as mp
warnings.filterwarnings("ignore")

def generate_conjunction_fact(table_data, fact_template, type):
    '''
    "fact_template": "The [target_col] that have [condition] are [executed_results]."
    '''
    table = WikiTable(table_data)
    
    target_col_idx = table.key_column_idx
    target_col_name = table.header[target_col_idx]
    
    # Generate a single condition
    condition, answer_row_ids = generate_condition(table, target_col_idx)
    
    if condition is not None:
        fact = fact_template.replace("[condition]", condition)
        fact = fact.replace("[target_col]", target_col_name)
        
        executed_results = [table.rows[i][target_col_idx] for i in answer_row_ids]
        executed_results = table.unify_answers(executed_results)
        fact = fact.replace("[executed_results]", ", ".join(executed_results))
        
        return fact
    else:
        return None

def main():
    # Load your table data and fact templates here
    table_data = "Your table data here"
    fact_template = "The [target_col] that have [condition] are [executed_results]."
    
    # Example of calling the generate_conjunction_fact function
    fact = generate_conjunction_fact(table_data, fact_template, 'conjunction')
    if fact:
        print("Generated Fact:", fact)
    else:
        print("No fact could be generated.")

if __name__ == "__main__":
    main()
