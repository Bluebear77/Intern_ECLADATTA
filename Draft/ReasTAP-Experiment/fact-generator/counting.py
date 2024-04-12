from utils.generate_condition import *
from utils.table_wrapper import WikiTable
import random

def generate_counting_fact(table_data, fact_template, type, count_map={"counting_1": 1, "counting_2": 2}):
    
    """
    fact_template: "[executed_results] [target_col] have [source_col] [condition]."
   
    """

    table = WikiTable(table_data)
    
    # Use count_map to determine the number of source columns to use based on the type
    source_col_count = count_map.get(type, 1)  # Default to 1 column if type is not specified
    source_cols = sample_source_cols(table, source_col_count)
    if source_cols is None:
        return None, None

    # Determine the target column, assuming the key column index points to the target column
    target_col_idx = table.key_column_idx
    target_col_name = table.header[target_col_idx]

    # Generate conditions based on the type and sampled columns
    if type == "counting_1":
        cond, ans_ids = generate_condition(source_cols[0]["column_data"], source_cols[0]["type"])
        if not cond:
            return None, None
    elif type == "counting_2":
        if len(source_cols) < 2:
            return None, None  # Ensure two columns are available
        cond, cond2, ans_ids = generate_joint_condition(source_cols[0]["column_data"], source_cols[1]["column_data"], source_cols[0]["type"], source_cols[1]["type"])
        if not cond or not cond2:
            return None, None

    # Format the fact based on the template
    executed_results = len(ans_ids)
    fact = fact_template.replace("[executed_results]", str(executed_results))
    fact = fact.replace("[target_col]", target_col_name)
    fact = fact.replace("[source_col]", source_cols[0]["column_name"])
    fact = fact.replace("[condition]", cond)
    if type == "counting_2":
        fact = fact.replace("[condition_2]", cond2)
        fact = fact.replace("[source_col_2]", source_cols[1]["column_name"])

    return fact, executed_results
