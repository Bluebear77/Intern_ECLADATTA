def generate_fact(table_data, fact_template):
    """
    Generates a factual statement from the given table data based on specified conditions.
    
    Args:
        table_data (list of dicts): The data of the table in the form of a list of dictionaries.
        fact_template (str): A template for the fact to generate, with placeholders.

    Returns:
        str: A factual statement generated based on the table data.
    """
    # Assuming a WikiTable class and some necessary functions are defined elsewhere
    table = WikiTable(table_data)

    # Randomly select one column to be the source of conditions
    source_col = sample_source_col(table)  # Function to select one column for condition
    if source_col is None:
        return None

    # Target column is assumed to be another column; selecting it randomly or specifically
    target_col = sample_target_col(table)  # Function to select target column
    
    # Assuming a function to generate a condition and get the rows meeting this condition
    cond, executed_row_ids = generate_condition(source_col["column_data"], source_col["type"])

    if cond is None:
        return None
    
    # Generate the factual statement
    executed_results = [table.rows[i][target_col["column_idx"]] for i in executed_row_ids]
    executed_results = ', '.join(set(executed_results))  # Ensure results are unique and convert to string

    fact = fact_template.replace("[target_col]", target_col["column_name"])
    fact = fact.replace("[cond]", f"{source_col['column_name']} is {cond}")
    fact = fact.replace("[executed_results]", executed_results)

    return fact

# Auxiliary functions like sample_source_col, sample_target_col, generate_condition must be defined.import random
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

