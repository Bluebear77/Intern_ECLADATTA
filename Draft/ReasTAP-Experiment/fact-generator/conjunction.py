def generate_fact(table_data, fact_template):
    """
   
    fact template:The `col1` that have `CONDITION` are `executed_results`.

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
