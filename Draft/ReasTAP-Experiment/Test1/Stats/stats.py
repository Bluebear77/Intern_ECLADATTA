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
    
    # Process each file
    for i in range(start, end + 1):
        file_path = os.path.join(base_path, f'instance_{i}_processed_output.json')
        total_questions, reasoning_type_counts = process_file(file_path)
        
        # Update global stats
        global_total_questions += total_questions
        global_reasoning_type_counts.update(reasoning_type_counts)
        
        # Write stats to individual markdown file
        write_stats_markdown(stats_dir, i, total_questions, reasoning_type_counts)
    
    # Write combined stats to markdown file
    write_stats_markdown(stats_dir, 'all', global_total_questions, global_reasoning_type_counts)

def process_file(filepath):
    with open(filepath, 'r') as file:
        data = json.load(file)
    
    total_questions = 0
    reasoning_type_counts = Counter()
    
    for item in data:
        total_questions += len(item["qas"])
        reasoning_types = [qa['reasoning_type'] for qa in item["qas"]]
        reasoning_type_counts.update(reasoning_types)
    
    return total_questions, reasoning_type_counts


def write_stats_markdown(directory, index, total_questions, reasoning_type_counts):
    filename = os.path.join(directory, f'stats_{index}.md')
    with open(filename, 'w') as md_file:
        md_file.write(f"# Statistics for Instance {index}<br/>\n")
        md_file.write(f"Total number of questions: {total_questions}<br/>\n")
        md_file.write(f"Total {len(reasoning_type_counts)} unique reasoning types are produced.<br/>\n")
        md_file.write("## Reasoning Type Statistics<br/>\n")
        for rtype, count in reasoning_type_counts.items():
            percentage = (count / total_questions) * 100
            md_file.write(f"- **{rtype}:** Count = {count}, Percentage = {percentage:.2f}%<br/>\n")

# Specify the base directory where files are located
base_path = "../"

# Analyze JSON files from instance 1 to 100
analyze_json_files(base_path, 1, 100)
