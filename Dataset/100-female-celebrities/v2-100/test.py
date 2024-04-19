import re
import json



def extract_table_data(table):
    headers = re.findall(r'^\!\s*(.*)', table, re.MULTILINE)
    headers = [clean_text(h.split('!!')[0]) for h in headers]

    rows = []
    spans = [0] * len(headers)  # Initialize spans to match the number of headers
    actual_rows = table.split('|-')[1:]

    for row in actual_rows:
        cells = re.split(r'\n\|', row)[1:]
        row_result = [''] * len(headers)  # Initialize row_result with empty strings for each header
        col_index = 0

        for cell in cells:
            while col_index < len(headers) and spans[col_index] > 0:
                spans[col_index] -= 1
                col_index += 1  # Move to next column if current is spanned from previous row

            # Handle rowspan
            span_match = re.search(r'rowspan="(\d+)"', cell)
            if span_match:
                span_length = int(span_match.group(1)) - 1
                spans[col_index] = span_length

            clean_cell = clean_text(cell)
            if col_index < len(headers):  # Check to prevent out of range error
                row_result[col_index] = clean_cell
            col_index += 1

        rows.append(row_result)
        spans = [max(0, x - 1) for x in spans]  # Reduce spans for next row

    # Determine data types and numeric columns
    data_types = determine_data_types(rows)
    numeric_columns = [index for index, type in enumerate(data_types) if type == 'numeric']
    key_column = numeric_columns[0] if numeric_columns else None

    return headers, rows, data_types, key_column, numeric_columns

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
                column_types[i] = 'date'
            elif column_types[i] == 'text' and re.match(r'\d{4}', cell):
                column_types[i] = 'year'
    return column_types

def is_numeric(text):
    try:
        float(text.replace(',', '').replace(' ', ''))
        return True
    except ValueError:
        return False

def clean_text(text):
    # Cleaning function as per your requirement
    text = re.sub(r'<[^>]*>', '', text)
    text = re.sub(r'\[\[([^|\]]*\|)?([^\]]+)\]\]', r'\2', text)
    text = re.sub(r'\{\{[^}]+\}\}', '', text)
    text = re.sub(r'rowspan="\d+"', '', text)
    text = re.sub(r'align="center"', '', text)
    text = re.sub(r'\'{2,}', '', text)
    text = re.sub(r'\|', '', text)
    return text.strip()


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
