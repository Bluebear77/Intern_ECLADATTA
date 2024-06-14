import re

def split_dev_log(input_file):
    with open(input_file, 'r') as file:
        lines = file.readlines()
    
    output_files = {}
    current_lines = []
    current_file = None

    for line in lines:
        current_lines.append(line)
        match = re.search(r'Saved data to \.\/test\/(qtsumm_dev_chunk_\d+\.csv)', line)
        if match:
            current_file = match.group(1).replace('.csv', '.txt')
            output_files[current_file] = current_lines
            current_lines = []

    # Write to output files
    for file_name, content in output_files.items():
        with open(file_name, 'w') as f:
            f.writelines(content)

if __name__ == "__main__":
    split_dev_log('test-log.txt')
