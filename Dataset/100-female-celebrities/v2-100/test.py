import re
import json

def clean_text(text):
    text = re.sub(r'<[^>]*>', '', text)
    text = re.sub(r'\[\[([^|\]]*\|)?([^\]]+)\]\]', r'\2', text)
    text = re.sub(r'\{\{[^}]+\}\}', '', text)
    text = re.sub(r'rowspan="\d+"', '', text)
    text = re.sub(r'align="center"', '', text)  # Remove align="center" from the text
    text = re.sub(r'\'{2,}', '', text)  # Removes multiple single quotes used for italic in wiki markup
    text = re.sub(r'\|', '', text)  # Removes all "|" characters
    return text.strip()

def is_numeric(text):
    try:
        float(text.replace(',', '').replace(' ', ''))
        return True
    except ValueError:
        return False

def determine_data_types(rows):
    if not rows:
        return []
    column_count = len(rows[0])
    column_types = ['text'] * column_count
    for row in rows:
        for i, cell in enumerate(row):
            if is_numeric(cell):
                column_types[i] = 'numeric'
            elif re.match(r'\d{4}-\d{2}-\d{2}', cell):
                column_types[i] = 'date'  # Identify ISO date formats
            elif column_types[i] == 'text' and re.match(r'\d{4}', cell):
                column_types[i] = 'year'  # A column containing just years
    return column_types

def extract_table_data(table):
    headers = re.findall(r'^\!\s*(.*)', table, re.MULTILINE)
    headers = [clean_text(h.split('!!')[0]) for h in headers]

    rows = []
    spans = [0] * len(headers)
    actual_rows = table.split('|-')[1:]

    for row in actual_rows:
        cells = re.split(r'\n\|', row)[1:]
        row_result = []
        col_index = 0

        for cell in cells:
            #print(f"Processing cell: {cell}")  # Debug print
            while col_index < len(spans) and spans[col_index] > 0:
                row_result.append('')
                spans[col_index] -= 1
                col_index += 1

            span_match = re.search(r'rowspan="(\d+)"', cell)
            span_length = 0
            if span_match:
                span_length = int(span_match.group(1)) - 1
                print(f"span_match found, col_index: {col_index}, span_length: {span_length}, spans length: {len(spans)}")  # Debug print
                if col_index < len(spans):
                    spans[col_index] = span_length
                else:
                    print("Error: col_index out of range of spans")  # Error notice

            clean_cell = clean_text(cell.strip())  # Apply the cleaning including removal of "|"
            row_result.append(clean_cell)
            if span_length > 0 and col_index < len(spans):
                spans[col_index] = span_length

            col_index += 1

            #print(f"Current row_result: {row_result}")  # Debug print
            #print(f"Current spans state: {spans}")  # Debug print

        spans = [max(0, x - 1) for x in spans]
        rows.append(row_result)

    data_types = determine_data_types(rows)
    numeric_columns = [index for index, type in enumerate(data_types) if type == 'numeric']
    key_column = numeric_columns[0] if numeric_columns else None

    return headers, rows, data_types, key_column, numeric_columns

def extract_wiki_table_data(content):
    tables = re.findall(r'\{\|\s*class="[^"]*wikitable[^"]*"(.*?)\|\}', content, re.DOTALL)
    all_tables = []

    for table in tables:
        headers, rows, column_types, key_column, numeric_columns = extract_table_data(table)
        all_tables.append({
            'header': headers,
            'rows': rows,
            'column_types': column_types,
            'key_column': key_column,
            'numeric_columns': numeric_columns
        })

    return all_tables

# Specify file paths
files = [("P2/tables_output-instance_{}.txt".format(i), "P3/output_instance_{}.json".format(i)) for i in range(1, 3)]

# Process each file and save the output to new JSON files
for input_path, output_path in files:
    try:
        with open(input_path, 'r', encoding='utf-8') as file:
            file_content = file.read()
            result = extract_wiki_table_data(file_content)
            if result:
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(result, f, indent=4, ensure_ascii=False)
                print(f"Data successfully saved to {output_path}")
            else:
                print(f"Failed to process {input_path}: No data found")
    except FileNotFoundError:
        print(f"File not found: {input_path}")
    except Exception as e:
        print(f"An error occurred while processing {input_path}: {str(e)}")
