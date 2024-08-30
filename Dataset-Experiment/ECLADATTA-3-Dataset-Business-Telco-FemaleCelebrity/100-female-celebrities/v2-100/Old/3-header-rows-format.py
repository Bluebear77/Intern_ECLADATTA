import re
import json

import re

def clean_text(text):
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    # Remove wiki markup like [[Page|Display]] and replace with 'Display'
    text = re.sub(r'\[\[([^|\]]*\|)?([^\]]+)\]\]', r'\2', text)
    # Remove templates and nested templates recursively
    while re.search(r'\{\{[^{}]+\}\}', text):
        text = re.sub(r'\{\{[^{}]+\}\}', '', text)
    # Remove style and class attributes
    text = re.sub(r'\b(style|class)="[^"]*"', '', text)
    # Remove extraneous characters like brackets which might not be needed
    text = re.sub(r'[\|\[\]\{\}]', '', text)
    # Normalize whitespace to a single space
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def extract_wiki_table_data(file_content):
    #tables = re.findall(r'\{\|\s*class="[^"]*wikitable[^"]*"(.*?)(?=\{\||\Z)', file_content, re.DOTALL)
    tables = re.findall(r'\{\|\s*(?:[^|\n]*?\s+)?class="[^"]*wikitable[^"]*"(.*?)(?=\{\||\Z)', file_content, re.DOTALL)
    
     
    if not tables:
        return None, "No tables found"
    
    results = []
    log_messages = []

    for table in tables:
        headers = re.search(r'\n\!(.*?)\n\|-\n', table, re.DOTALL)
        
        if headers:
            headers = [clean_text(h) for h in headers.group(1).split('!')]
            
        else:
            log_messages.append("No headers found in table")
            continue

        rows = re.findall(r'\|\-\s*(?:\|\s*rowspan="\d+"\s*\|)?(.*?)\n(?=\|\-|\|\})', table, re.DOTALL)
        
        parsed_rows = []

        for row in rows:
            entries = [clean_text(entry) for entry in row.split('\n|')]
            parsed_rows.append(entries)

        results.append({
            "header": headers,
            "rows": parsed_rows
        })

    return results, "\n".join(log_messages)

# Specify file paths
files = [("P2/tables_output-instance_{}.txt".format(i), "P3/output_instance_{}.json".format(i)) for i in range(1, 101)]

log_entries = []
for input_path, output_path in files:
    try:
        with open(input_path, 'r', encoding='utf-8') as file:
            file_content = file.read()
            result, log_message = extract_wiki_table_data(file_content)
            log_entries.append(f"Processing {input_path}\n{log_message}")
            
            if result:
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(result, f, indent=4, ensure_ascii=False)
                log_entries.append(f"Data successfully saved to {output_path}")
            else:
                log_entries.append(f"Failed to process {input_path}: No data found")
    except FileNotFoundError:
        log_entries.append(f"File not found: {input_path}")
    except Exception as e:
        log_entries.append(f"An error occurred while processing {input_path}: {str(e)}")

with open('log.md', 'w', encoding='utf-8') as log_file:
    log_file.write("\n\n".join(log_entries))