import json
import os
import pandas as pd

def extract_typing_labels(json_file):
    with open(json_file, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    results = []
    logs = []

    extraction_metadata = data["_source"]["extractionMetadata"]
    preprocessing_metadata = data["_source"]["preprocessingMetadata"]
    
    tables = extraction_metadata[0]["tables"]
    tech_results = preprocessing_metadata[0]["technologyResults"]
    
    tech_results_dict = {tr["index"]: tr for tr in tech_results}
    
    for table in tables:
        table_num = table["tableNum"]
        print(f"Processing tableNum: {table_num}")
        if table_num in tech_results_dict:
            tech_result = tech_results_dict[table_num]
            if "dagobah" in tech_result and "preprocessed" in tech_result["dagobah"]:
                if "primitiveTyping" in tech_result["dagobah"]["preprocessed"]:
                    primitive_typing = tech_result["dagobah"]["preprocessed"]["primitiveTyping"]
                    max_column_index = max([col["columnIndex"] for col in primitive_typing]) + 1
                    column_types = ["UNKNOWN"] * max_column_index
                    for column in primitive_typing:
                        column_index = column["columnIndex"]
                        if column["typing"]:
                            column_type = column["typing"][0]["typingLabel"]
                            if column_type == 'DATE':
                                column_type = 'datetime'
                            column_types[column_index] = column_type
                    results.append([table_num, max_column_index] + column_types)
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
    
    if results:
        max_columns = max([len(row) for row in results]) - 2
        headers = ["TableNum", "column_number"] + [f"column_type_{i+1}" for i in range(max_columns)]
        df = pd.DataFrame(results, columns=headers)
    else:
        df = None

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

def process_files(json_file_path, csv_file_path, output_file_path, error_log):
    try:
        csv_data = pd.read_csv(csv_file_path)
        
        with open(json_file_path, 'r', encoding='utf-8') as f:
            json_data = json.load(f)

        grouped_csv_data = csv_data.groupby('TableNum')

        for table_num, table_data in enumerate(json_data):
            if table_num in grouped_csv_data.groups:
                table_csv_data = grouped_csv_data.get_group(table_num)
                assert len(table_csv_data) == 1, "Multiple rows found for the same TableNum"
                table_csv_row = table_csv_data.iloc[0]

                column_types = [table_csv_row[f'column_type_{i}'] for i in range(1, table_csv_row['column_number'] + 1)]
                key_column = int(table_csv_row['key column']) if not pd.isna(table_csv_row['key column']) else ""

                table_data['column_types'] = column_types
                table_data['key_column'] = key_column

        with open(output_file_path, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, indent=4, default=str)
    
    except ValueError as e:
        if 'cannot convert float NaN to integer' in str(e):
            with open(error_log, 'a', encoding='utf-8') as log_file:
                log_file.write(f'Skip due to missing key column: {csv_file_path}\n')



def main():
    input_dir = './Raw/'
    output_dir = './CSV/'
    processed_dir = './P2/'
    final_output_dir = './P4/'
    log_file_path = os.path.join(output_dir, 'log.txt')
    error_log = os.path.join(final_output_dir, 'log.txt')

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    if not os.path.exists(final_output_dir):
        os.makedirs(final_output_dir)

    all_logs = []

    for file_name in os.listdir(input_dir):
        if file_name.endswith('.json'):
            input_file_path = os.path.join(input_dir, file_name)
            instance_number = file_name.split('_')[1].split('.')[0]
            csv_file_path = os.path.join(output_dir, f'instance_{instance_number}.csv')

            df, logs = extract_typing_labels(input_file_path)
            primary_key_positions = extract_key_column(input_file_path)
            
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

    with open(log_file_path, 'w', encoding='utf-8') as log_file:
        for log in all_logs:
            log_file.write(log + '\n')

    if os.path.exists(error_log):
        os.remove(error_log)

    for i in range(101):
        json_file_path = os.path.join(processed_dir, f'instance_{i}_processed.json')
        csv_file_path = os.path.join(output_dir, f'instance_{i}.csv')
        output_file_path = os.path.join(final_output_dir, f'instance_{i}_v4.json')
        
        if os.path.exists(json_file_path) and os.path.exists(csv_file_path):
            process_files(json_file_path, csv_file_path, output_file_path, error_log)

# Run the main function
main()

