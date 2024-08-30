import json

# List of JSON files to scan
json_files = ["../../qtsumm_dev.json", "../../qtsumm_test.json", "../../qtsumm_train.json"]

def count_unique_tables(files, key):
    overall_unique_values = set()  # Set to store unique values across all files
    file_unique_counts = []  # List to store unique counts for each file

    for file_path in files:
        try:
            with open(file_path, 'r') as file:  # Open the JSON file
                data = json.load(file)  # Load the data from the JSON file
            # Collect unique values for the specified key from the current file
            file_unique = set(item['table'][key] for item in data)
            overall_unique_values.update(file_unique)  # Update the combined unique values set
            # Append the count of unique values for the current file to the list
            file_unique_counts.append((file_path, len(file_unique)))
        except Exception as e:
            print(f"Error processing file {file_path}: {e}")  # Print error message if any
            file_unique_counts.append((file_path, 0))  # Append zero if there's an error

    return file_unique_counts, len(overall_unique_values)  # Return the individual and total unique counts

# Calculate unique tables based on 'table_id' and 'title' respectively
unique_table_ids_counts, total_unique_table_ids = count_unique_tables(json_files, 'table_id')
unique_titles_counts, total_unique_titles = count_unique_tables(json_files, 'title')

# Print individual file counts for 'table_id'
for file, count in unique_table_ids_counts:
    print(f"File: {file}")
    print(f"Number of unique tables based on 'table_id': {count}")

# Print individual file counts for 'title'
for file, count in unique_titles_counts:
    print(f"File: {file}")
    print(f"Number of unique tables based on 'title': {count}")

print("-" * 40)  # Print a separator line

# Print total unique counts across all files
print(f"Total number of unique tables based on 'table_id' across all files: {total_unique_table_ids}")
print(f"Total number of unique tables based on 'title' across all files: {total_unique_titles}")

