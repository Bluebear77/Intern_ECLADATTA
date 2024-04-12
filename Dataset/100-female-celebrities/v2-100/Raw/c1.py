import json
import re

def extract_wikitables(content):
    table_pattern = re.compile(r'\n==[^=]+==\n(\{\|.*?\n\|\})', re.DOTALL)
    tables = table_pattern.findall(content)
    return tables

def parse_table(table_content):
    rows = re.sub(r'(^\{\||\|\}$)', '', table_content, flags=re.MULTILINE).strip().split("\n|-")
    table_data = []
    for row in rows:
        cells = re.findall(r'\|\s*(.*?)\s*(?=\n|$)', row)
        cells = [re.sub(r'\[\[(?:[^\]|]*\|)?([^\]]+)\]\]', r'\1', cell).strip() for cell in cells]
        if cells:
            table_data.append(cells)
    return table_data

def process_json_file(file_path, output_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            content = data['_source']['contentMetadata']['content']
            identification = data['_source']['identificationMetadata']
            tables = extract_wikitables(content)
            results = []
            for idx, table in enumerate(tables):
                table_data = parse_table(table)
                json_file = f"{output_path}_table_{idx+1}.json"
                table_info = {
                    'id': identification['id'],
                    'title': identification['title'],
                    'url': identification['url'],
                    'table': table_data
                }
                with open(json_file, 'w', encoding='utf-8') as jsonfile:
                    json.dump(table_info, jsonfile, ensure_ascii=False, indent=4)
                results.append(json_file)
            return f"Tables and metadata have been successfully written to JSON files: {results}"
    except KeyError as e:
        return f"KeyError: The key {e} was not found in the JSON structure."
    except FileNotFoundError:
        return "Error: The file was not found. Check the file path."
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Example usage
file_path = 'instance_36.json'  # Update this with the correct file path
output_path = 'output.json'     # Base name for output files
result = process_json_file(file_path, output_path)
print(result)
