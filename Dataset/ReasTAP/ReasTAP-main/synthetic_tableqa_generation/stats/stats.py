import json
from collections import Counter
import os

def analyze_json_files(base_path, start, end):
    # Prepare directory for output markdown files
    stats_dir = os.path.join(base_path, 'Stats')
    os.makedirs(stats_dir, exist_ok=True)
    
    # Initialize global reasoning type counter and total questions
    global_reasoning_type_counts = Counter()
    global_total_questions = 0
    global_total_tables = 0
    
    # Count the total number of JSON files in the base path
    total_pages = sum(1 for file in os.listdir(base_path) if file.endswith('.json'))
    
    # Process each file
    for i in range(start, end + 1):
        file_path = os.path.join(base_path, f'synthetic_qa_output_instance_{i}_v5.json')
        
        try:
            total_questions, total_tables, reasoning_type_counts = process_file(file_path)
            
            # Update global stats
            global_total_questions += total_questions
            global_total_tables += total_tables
            global_reasoning_type_counts.update(reasoning_type_counts)
            
            # Write stats to individual markdown file
            write_stats_markdown(stats_dir, i, total_questions, total_tables, reasoning_type_counts)
        except FileNotFoundError:
            print(f"File not found: {file_path}, skipping.")
    
    # Write combined stats to markdown file
    write_stats_markdown(stats_dir, 'all', global_total_questions, global_total_tables, global_reasoning_type_counts, total_pages)

def process_file(filepath):
    with open(filepath, 'r') as file:
        data = json.load(file)
    
    total_questions = 0
    total_tables = 0
    reasoning_type_counts = Counter()
    
    for item in data:
        total_questions += len(item["qas"])
        total_tables += 1  # Each item is considered as a table
        reasoning_types = [qa['reasoning_type'] for qa in item["qas"]]
        reasoning_type_counts.update(reasoning_types)
    
    return total_questions, total_tables, reasoning_type_counts

def write_stats_markdown(directory, index, total_questions, total_tables, reasoning_type_counts, total_pages=None):
    filename = os.path.join(directory, f'stats_{index}.md')
    with open(filename, 'w') as md_file:
        if total_pages is not None and index == 'all':
            md_file.write(f"# Statistics for Instance {index}<br/>\n")
            md_file.write(f"Total number of pages: {total_pages}<br/>\n")
        else:
            md_file.write(f"# Statistics for Instance {index}<br/>\n")
        md_file.write(f"Total number of questions: {total_questions}<br/>\n")
        md_file.write(f"Total number of tables: {total_tables}<br/>\n")
        md_file.write(f"Total {len(reasoning_type_counts)} unique reasoning types are produced.<br/>\n")
        md_file.write("## Reasoning Type Statistics<br/>\n")
        for rtype, count in reasoning_type_counts.items():
            percentage = (count / total_questions) * 100
            md_file.write(f"- **{rtype}:** Count = {count}, Percentage = {percentage:.2f}%<br/>\n")
        if total_pages is not None and index != 'all':
            md_file.write(f"Total number of pages: {total_pages}<br/>\n")

# Specify the base directory where files are located
base_path = "../output-telco-100"

# Analyze JSON files from instance 1 to 100
analyze_json_files(base_path, 1, 100)
