import csv

# Function to read URLs from a CSV file and return filtered rows where the title contains "liste des"
def read_and_filter_urls_from_csv(csv_file_path):
    filtered_rows = []
    with open(csv_file_path, mode='r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            # Check if 'liste des' is in the title (first column) using a case-insensitive comparison
            if 'liste des' in row[0].lower():
                filtered_rows.append(row)
    return filtered_rows

# Function to write the filtered data to a CSV file
def write_to_csv(output_file_path, data):
    with open(output_file_path, mode='w', encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Name", "URL1", "URL2", "Categories"])  # Adjust column names as needed
        writer.writerows(data)

# File paths
input_csv_path = 'extracted_all.csv'  # Update this to the correct path of your input CSV
output_csv_path = 'list-extracted_data.csv'  # Path for the output CSV file

# Read and filter URLs from the CSV file
filtered_data = read_and_filter_urls_from_csv(input_csv_path)

# Write the filtered data to the output CSV file
write_to_csv(output_csv_path, filtered_data)

print(f"Filtering completed. Data saved to {output_csv_path}.")

