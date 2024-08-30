import os
import csv

# Define the directory containing all the `.csv` files to be merged
base_directory = '.'

# Initialize an empty list to store the rows from all `.csv` files
all_data = []

# List the files in the base directory
files = os.listdir(base_directory)

# Collect all `.csv` files that end with '.csv'
csv_files = [file for file in files if file.endswith('.csv')]

# Process each `.csv` file
for csv_file in csv_files:
    csv_file_path = os.path.join(base_directory, csv_file)
    with open(csv_file_path, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        header = next(reader, None)  # Skip the header row if present
        for row in reader:
            all_data.append(row)

# Write all the merged data to a single `.csv` file
output_csv_path = os.path.join(base_directory, 'WTQ.csv')
with open(output_csv_path, mode='w', newline='', encoding='utf-8') as output_file:
    writer = csv.writer(output_file)
    writer.writerow(['URL'])  # Adjust the header as needed
    writer.writerows(all_data)

print(f'Successfully merged all CSV files into {output_csv_path}')
