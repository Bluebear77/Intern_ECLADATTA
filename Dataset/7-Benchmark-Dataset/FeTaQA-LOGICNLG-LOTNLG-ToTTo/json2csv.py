import json
import csv

# Load JSON data
with open('qtsumm_train.json', 'r') as json_file:
    data = json.load(json_file)

# Open a CSV file for writing
with open('qtsumm_train.csv', 'w', newline='', encoding='utf-8') as csv_file:
    # Create a CSV writer
    csv_writer = csv.writer(csv_file)
    
    # Write the header
    csv_writer.writerow(['Example ID', 'Table ID', 'Table Title', 'Query', 'Summary', 'Header', 'Rows'])
    
    # Write data rows
    for entry in data:
        example_id = entry['example_id']
        table_id = entry['table']['table_id']
        title = entry['table']['title']
        query = entry['query']
        summary = entry['summary']
        header = "; ".join(entry['table']['header'])  # Joining table headers with "; "
        rows = ["; ".join(row) for row in entry['table']['rows']]  # Joining each row's cells with "; "
        rows_str = "| ".join(rows)  # Separating rows with "| "
        
        # Write row to CSV
        csv_writer.writerow([example_id, table_id, title, query, summary, header, rows_str])
