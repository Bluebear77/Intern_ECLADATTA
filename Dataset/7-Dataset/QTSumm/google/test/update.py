import pandas as pd
from fuzzywuzzy import fuzz
import glob

def extract_first_4x4(df):
    return df.iloc[:4, :4]

def compare_tables(actual_df, matched_df):
    actual_sub = extract_first_4x4(actual_df)
    matched_sub = extract_first_4x4(matched_df)
    if actual_sub.empty or matched_sub.empty:
        return 0.0
    return fuzz.ratio(actual_sub.to_string(index=False, header=True), matched_sub.to_string(index=False, header=True))

def parse_text_file(text_file):
    with open(text_file, 'r') as file:
        lines = file.readlines()

    tables_info = []
    current_table = None
    is_actual_table = False
    is_matched_table = False
    for line in lines:
        if line.startswith("Table_id:"):
            if current_table:
                tables_info.append(current_table)
            current_table = {"table_id": line.split(":")[1].strip(), "actual": [], "matched": []}
            is_actual_table = False
            is_matched_table = False
        elif line.startswith("Actual table"):
            is_actual_table = True
            is_matched_table = False
        elif line.startswith("Most similar table"):
            is_actual_table = False
            is_matched_table = True
        elif line.strip() == "":
            continue
        elif current_table:
            if is_actual_table:
                current_table["actual"].append(line.strip())
            elif is_matched_table:
                current_table["matched"].append(line.strip())
    if current_table:
        tables_info.append(current_table)
    return tables_info

def table_to_df(table_lines):
    if not table_lines:
        return pd.DataFrame()

    # Extract the header
    header = table_lines[0].split()
    num_columns = len(header)

    # Extract the data
    data = []
    for line in table_lines[1:]:
        row = line.split(maxsplit=num_columns-1)  # Ensure split into the correct number of columns
        if len(row) == num_columns:
            data.append(row)
        else:
            # Handle rows with unexpected number of columns
            row += [''] * (num_columns - len(row))  # Pad with empty strings if columns are missing
            data.append(row)

    return pd.DataFrame(data, columns=header)

# Get all text and csv files
text_files = sorted(glob.glob("qtsumm_test_chunk_*.txt"))
csv_files = sorted(glob.glob("qtsumm_test_chunk_*.csv"))

# Process each pair of text and csv files
for text_file, csv_file in zip(text_files, csv_files):
    # Load the text file and parse the table information
    tables_info = parse_text_file(text_file)
    
    # Load the CSV file
    df = pd.read_csv(csv_file)
    
    # Update the CSV file with the table similarities
    for table_info in tables_info:
        table_id = table_info["table_id"]
        actual_df = table_to_df(table_info["actual"])
        matched_df = table_to_df(table_info["matched"])
        
        table_similarity = compare_tables(actual_df, matched_df)
        df.loc[df['table_id'] == table_id, 'table_similarity'] = table_similarity
        
        # Update the overall similarity
        df.loc[df['table_id'] == table_id, 'overall_similarity'] = (
            0.4 * df.loc[df['table_id'] == table_id, 'title_similarity'] + 0.6 * table_similarity
        ).astype(int)
    
    # Save the updated CSV file
    updated_csv_file = csv_file.replace(".csv", "_v2.csv")
    df.to_csv(updated_csv_file, index=False)
    print(f"Updated CSV file saved to {updated_csv_file}")
