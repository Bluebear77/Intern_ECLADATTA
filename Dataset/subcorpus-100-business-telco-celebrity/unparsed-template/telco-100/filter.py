import re
import csv
import os

# Function to extract only the highest-level template names
def extract_template_names_custom(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    matches = []
    stack = []
    in_template = False
    buffer = []
    depth = 0

    for i, char in enumerate(content):
        if char == '{' and i + 1 < len(content) and content[i + 1] == '{':
            if depth == 0:
                in_template = True
                buffer = []
            stack.append(char)
            depth += 1
        elif char == '}' and i + 1 < len(content) and content[i + 1] == '}':
            if depth > 0:
                depth -= 1
                stack.pop()
            if depth == 0 and in_template:
                in_template = False
                buffer_str = ''.join(buffer).strip()
                if buffer_str:
                    matches.append(buffer_str.split('|')[0].strip().lstrip('{'))
        if in_template:
            buffer.append(char)
    
    return matches

# Function to save template names to a CSV file
def save_to_csv(template_names, output_file):
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Template Name'])  # Write header
        for name in template_names:
            writer.writerow([name])

def main():
    input_directory = '.'
    # Get list of all .txt files and corresponding .csv files
    txt_files = [f for f in os.listdir(input_directory) if f.endswith('.txt')]
    csv_files = [f.replace('.csv', '.txt') for f in os.listdir(input_directory) if f.endswith('.csv')]

    # Identify .txt files that do not have a corresponding .csv file
    txt_files_to_process = [f for f in txt_files if f not in csv_files]

    for filename in txt_files_to_process:
        input_file = os.path.join(input_directory, filename)
        output_file = os.path.join(input_directory, filename.replace('.txt', '.csv'))
        
        template_names = extract_template_names_custom(input_file)
        
        save_to_csv(template_names, output_file)
        print(f"Extracted {len(template_names)} template names from {filename} and saved to {output_file}")

if __name__ == "__main__":
    main()
