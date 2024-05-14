import os
import pandas as pd

# Directory containing the CSV files
directory = "."

# Get the list of CSV files, excluding summary.csv
csv_files = [f for f in os.listdir(directory) if f.endswith('.csv') and f != 'summary.csv']

# Extract dataset names without the .csv extension
dataset_names = [os.path.splitext(f)[0] for f in csv_files]

# Initialize a dictionary to store URLs for each file
url_dict = {}

# Read URLs from each file
for file in csv_files:
    df = pd.read_csv(os.path.join(directory, file))
    urls = df.iloc[:, 0].dropna().tolist()
    url_dict[os.path.splitext(file)[0]] = set(urls)

# Create a DataFrame to store the overlap counts
overlap_matrix = pd.DataFrame(index=dataset_names, columns=dataset_names)

# Compare URLs between each pair of files
for file1 in dataset_names:
    for file2 in dataset_names:
        if file1 == file2:
            overlap_matrix.loc[file1, file2] = ''
        else:
            overlap_count = len(url_dict[file1].intersection(url_dict[file2]))
            overlap_matrix.loc[file1, file2] = overlap_count

# Save the overlap matrix to a CSV file
overlap_matrix.to_csv(os.path.join(directory, 'summary.csv'))
