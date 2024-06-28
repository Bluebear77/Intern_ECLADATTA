import json
import os
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
                            column_type = column["typing"][0]["typingLabel"]  # take the first typingLabel
                            if column_type == 'DATE':
                                column_type = 'datetime'
                            column_types[column_index] = column_type
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
        df = None  # Return None if no results

    return df, logs

def extract_key_column(json_file):
    with open(json_file, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    primary_key_positions = {}
    preprocessing_metadata = data['_source'].get('preprocessingMetadata', [])
    
    for tech_result in preprocessing_metadata:
        if 'technologyResults' in tech_result:
            tech_results = tech_result['technologyResults']
            for result in tech_results:
                if ('dagobah' in result and 
                    'preprocessed' in result['dagobah'] and
                    'primaryKeyInfo' in result['dagobah']['preprocessed']):
                    
                    preprocessed = result['dagobah']['preprocessed']
                    primary_key_position = preprocessed['primaryKeyInfo'].get('primaryKeyPosition')
                    index = result['index']
                    primary_key_positions[index] = primary_key_position

    return primary_key_positions

# Main function to read JSON and output CSV and log for all input files
def main():
    input_dir = './Raw/'
    output_dir = './CSV/'
    log_file_path = os.path.join(output_dir, 'log.txt')

    # Ensure output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    all_logs = []

    for file_name in os.listdir(input_dir):
        if file_name.endswith('.json'):
            input_file_path = os.path.join(input_dir, file_name)
            instance_number = file_name.split('_')[1].split('.')[0]
            csv_file_path = os.path.join(output_dir, f'instance_{instance_number}.csv')

            df, logs = extract_typing_labels(input_file_path)
            primary_key_positions = extract_key_column(input_file_path)
            
            # Collect logs
            all_logs.extend(logs)
            
            if df is not None and not df.empty:
                table_nums = df['TableNum'].tolist()
                valid_tables = True
                
                for table_num in table_nums:
                    if table_num not in primary_key_positions:
                        log_message = f"For file [{input_file_path}], table [{table_num}], primary key position not found."
                        print(log_message)
                        all_logs.append(log_message)
                        valid_tables = False
                        break

                if valid_tables:
                    df['key column'] = df['TableNum'].map(primary_key_positions)
                    df.to_csv(csv_file_path, index=False, encoding='utf-8')
                else:
                    log_message = f"For file [{input_file_path}], CSV not generated due to missing primary key position."
                    print(log_message)
                    all_logs.append(log_message)
            else:
                log_message = f"For file [{input_file_path}], no valid column type found."
                print(log_message)
                all_logs.append(log_message)

    # Save all logs to a single file
    with open(log_file_path, 'w', encoding='utf-8') as log_file:
        for log in all_logs:
            log_file.write(log + '\n')

# Run the main function
main()
