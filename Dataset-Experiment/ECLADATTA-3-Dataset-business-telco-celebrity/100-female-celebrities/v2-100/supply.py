import json
import pandas as pd
import os

def process_files(json_file_path, csv_file_path, output_file_path, error_log):
    try:
        # Load CSV file
        csv_data = pd.read_csv(csv_file_path)
        
        # Load JSON file
        with open(json_file_path, 'r') as f:
            json_data = json.load(f)

        # Group CSV data by TableNum
        grouped_csv_data = csv_data.groupby('TableNum')

        # Process each table in the JSON file
        for table_num, table_data in enumerate(json_data):
            if table_num in grouped_csv_data.groups:
                table_csv_data = grouped_csv_data.get_group(table_num)
                # Ensure only one row per TableNum
                assert len(table_csv_data) == 1, "Multiple rows found for the same TableNum"
                table_csv_row = table_csv_data.iloc[0]

                # Extract column types and key column
                column_types = [table_csv_row[f'column_type_{i}'] for i in range(1, table_csv_row['column_number'] + 1)]
                key_column = int(table_csv_row['key column'])

                # Update JSON data
                table_data['column_types'] = column_types
                table_data['key_column'] = key_column

        # Save the modified JSON file
        with open(output_file_path, 'w') as f:
            json.dump(json_data, f, indent=4, default=str)
    
    except ValueError as e:
        if 'cannot convert float NaN to integer' in str(e):
            with open(error_log, 'a') as log_file:
                log_file.write(f'Skip due to missing key column: {csv_file_path}\n')

# Define the log file path
error_log = './P4/log.txt'

# Clear the log file before running
if os.path.exists(error_log):
    os.remove(error_log)

# Process all instances
for i in range(101):  # Adjust the range as needed
    json_file_path = f'./P2/instance_{i}_processed.json'
    csv_file_path = f'./CSV/instance_{i}.csv'
    output_file_path = f'./P4/instance_{i}_v4.json'
    
    if os.path.exists(json_file_path) and os.path.exists(csv_file_path):
        process_files(json_file_path, csv_file_path, output_file_path, error_log)
