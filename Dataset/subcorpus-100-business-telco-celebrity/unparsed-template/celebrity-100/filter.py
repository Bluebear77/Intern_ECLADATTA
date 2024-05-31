import re
import csv

# Function to extract only the highest-level template names
def extract_template_names_custom(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    matches = []
    stack = []
    in_template = False
    buffer = []

    for i, char in enumerate(content):
        if char == '{' and i + 1 < len(content) and content[i + 1] == '{':
            if not in_template:
                in_template = True
                buffer = []
            stack.append(char)
        elif char == '}' and i + 1 < len(content) and content[i + 1] == '}':
            if stack:
                stack.pop()
            if not stack:
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

# Main function
def main():
    input_file = 'celebrity-04.txt'
    output_file = 'celebrity-04.csv'
    
    template_names = extract_template_names_custom(input_file)
    
    # Print first 10 rows of the output
    print("First 10 extracted template names:")
    for name in template_names[:10]:
        print(name)
    
    save_to_csv(template_names, output_file)
    print(f"Extracted {len(template_names)} template names and saved to {output_file}")

if __name__ == "__main__":
    main()
