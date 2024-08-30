import json
import csv

# Open the JSONL file and read lines
with open('unlabeled_totto_test_data.jsonl', 'r') as jsonl_file:
    lines = jsonl_file.readlines()

# Open a CSV file for writing
with open('unlabeled_totto_test_data.csv', 'w', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.writer(csv_file)
    # Write the header row
    csv_writer.writerow(['example_id', 'table_page_title', 'table_section_title', 'table_webpage_url', 'highlighted_cells', 'sentence_annotations'])

    for line in lines:
        data = json.loads(line)  # Load JSON object from a string
        
        # Extract relevant data
        example_id = data.get('example_id', '')
        table_page_title = data.get('table_page_title', '')
        table_section_title = data.get('table_section_title', '')
        table_webpage_url = data.get('table_webpage_url', '')
        
        # Convert highlighted_cells to a string for CSV
        highlighted_cells_str = str(data.get('highlighted_cells', []))
        
        # Extract and combine sentences from sentence_annotations
        sentence_annotations = data.get('sentence_annotations', [])
        sentences_combined = ' | '.join([ann['final_sentence'] for ann in sentence_annotations])
        
        # Write data row
        csv_writer.writerow([example_id, table_page_title, table_section_title, table_webpage_url, highlighted_cells_str, sentences_combined])
