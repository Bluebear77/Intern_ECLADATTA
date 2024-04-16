import re
import json

def extract_wiki_table_data(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            file_content = file.read()

        # Extract headers using regex
        header_pattern = r"\{\|\s*class=\"wikitable\"\s*\n\!(.*?)\n\|\-"
        header_match = re.search(header_pattern, file_content, re.DOTALL)
        headers = [h.strip() for h in re.split(r"!\s*align=\"[^\"]*\"\|", header_match.group(1)) if h.strip()]

        # Extract rows using regex
        row_pattern = r"\|\s*align=\"center\"\|\s*\[\[(\d{4}) en musique\|\d{4}\]\]\s*\|\s*align=\"center\"\|\s*''\[\[(.*?)\]\]''\s*\|\s*align=\"center\"\s*\|\s*\{\{nb\|(\d+)\}\}(?:<ref.*?>.*?</ref>)*\s*\|\s*align=\"center\"\|\s*(.*?)\s*\|-\s*"
        rows = re.findall(row_pattern, file_content, re.DOTALL)

        # Prepare JSON output structure
        json_output = {
            "header": headers,
            "rows": rows,
            "column_types": ["string", "string", "numeric", "string"],
            "key_column": 0,
            "numeric_columns": [2],
            "date_columns": {}
        }

        return json_output

    except Exception as e:
        print(f"Failed to process {file_path}: {str(e)}")
        return None

def save_to_json(data, output_path):
    try:
        with open(output_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        print(f"Data successfully saved to {output_path}")
    except Exception as e:
        print(f"Failed to save data: {str(e)}")

# Specify the paths to your files and the corresponding output file names
files = [
    ("P2/tables_output-instance_1.json", "output_instance_1.json"),
    ("P2/tables_output-instance_2.json", "output_instance_2.json")
]

# Process each file and save the output to new JSON files
for input_path, output_path in files:
    result = extract_wiki_table_data(input_path)
    if result:
        save_to_json(result, output_path)
