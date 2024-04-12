from utils.generate_condition import *
from utils.table_wrapper import WikiTable
import random

def generate_counting_fact(table_data, fact_template, type, count_map={"counting": 2}):
    """
    fact_template: "[executed_results] [target_col] have [source_col] [condition]."
   
    """
    table = WikiTable(table_data)
    
    # Attempt to select the source columns based on the type
    source_cols = sample_source_cols(table, count_map[type])
    if source_cols is None:
        return None, None
    
    # We assume the first column is the target for counting, and the second is the condition column
    target_col_idx = source_cols[0]["column_idx"]
    condition_col_idx = source_cols[1]["column_idx"]
    
    target_col_name = table.header[target_col_idx]
    condition_col_name = table.header[condition_col_idx]
    
    # Generate condition and identify answer rows
    cond, ans_ids = generate_condition(source_cols[1]["column_data"], source_cols[1]["type"])
    if not cond or not ans_ids:
        return None, None
    
    # Count the results
    executed_results = len(ans_ids)
    
    # Construct the fact using the template
    fact = fact_template.replace("[executed_results]", str(executed_results))
    fact = fact.replace("[target_col]", target_col_name)
    fact = fact.replace("[source_col]", condition_col_name)
    fact = fact.replace("[condition]", cond)

    return fact, executed_results

# Example usage: This would normally be wrapped in another function or module that handles the data input and iteration.
