import json
import pandas as pd

def extract_typing_labels(json_file):
    with open(json_file, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    # Initialize a list to store the results and logs
    results = []
    logs = []

    # Extract tables and technology results
    extraction_metadata = data["_source"]["extractionMetadata"]
    preprocessing_metadata = data["_source"]["preprocessingMetadata"]
    
    tables = extraction_metadata[0]["tables"]
    tech_results = preprocessing_metadata[0]["technologyResults"]
    
    # Create a dictionary for quick lookup of tech results by index
    tech_results_dict = {tr["index"]: tr for tr in tech_results}
    
    for table in tables:
        table_num = table["tableNum"]
        # Debugging information
        print(f"Processing tableNum: {table_num}")
        # Find corresponding tech result by index (same as table_num)
        if table_num in tech_results_dict:
            tech_result = tech_results_dict[table_num]
            if "dagobah" in tech_result and "preprocessed" in tech_result["dagobah"]:
                if "primitiveTyping" in tech_result["dagobah"]["preprocessed"]:
                    # Extract typing information
                    primitive_typing = tech_result["dagobah"]["preprocessed"]["primitiveTyping"]
                    max_column_index = max([col["columnIndex"] for col in primitive_typing]) + 1
                    column_types = ["UNKNOWN"] * max_column_index  # default to "UNKNOWN"
                    for column in primitive_typing:
                        column_index = column["columnIndex"]
                        if column["typing"]:
                            column_types[column_index] = column["typing"][0]["typingLabel"]  # take the first typingLabel
                    # Append the result for this table
                    results.append([table_num] + column_types)
                else:
                    log_message = f"For file [{json_file}], the table [{table_num}] no primitiveTyping data was found."
                    print(log_message)
                    logs.append(log_message)
            else:
                log_message = f"For file [{json_file}], the table [{table_num}] no preprocessed data was found in dagobah."
                print(log_message)
                logs.append(log_message)
        else:
            log_message = f"For file [{json_file}], the table [{table_num}] no matching tech result found."
            print(log_message)
            logs.append(log_message)
    
    # Create a DataFrame
    if results:
        max_columns = max([len(row) for row in results]) - 1
        headers = ["TableNum"] + [f"Column {i+1}" for i in range(max_columns)]
        df = pd.DataFrame(results, columns=headers)
    else:
        df = pd.DataFrame()  # Return an empty DataFrame if no results

    return df, logs

# Main function to read JSON and output CSV and log
def main():
    json_file = 'instance_47.json'
    output_csv = 'output.csv'
    output_log = 'log.txt'
    
    df, logs = extract_typing_labels(json_file)
    
    # Save to CSV
    df.to_csv(output_csv, index=False, encoding='utf-8')
    
    # Save logs to a file
    with open(output_log, 'w', encoding='utf-8') as log_file:
        for log in logs:
            log_file.write(log + '\n')
    
    return df, logs

df, logs = main()

import ace_tools as tools; tools.display_dataframe_to_user(name="Extracted Table Data", dataframe=df)

df, logs
