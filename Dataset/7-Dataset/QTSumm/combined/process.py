import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm
import numpy as np
import json
import os

# Part 1: Data Analysis and Statistics
# Load the data from the CSV files
input_files = ["qtsumm_dev.csv", "qtsumm_test.csv", "qtsumm_train.csv"]

# Read and concatenate the dataframes
df_list = [pd.read_csv(file) for file in input_files]
df = pd.concat(df_list, ignore_index=True)

# Calculate statistics
title_avg = df['title_similarity'].mean()
table_avg = df['table_similarity'].mean()
overall_avg = df['overall_similarity'].mean()

title_std = df['title_similarity'].std()
table_std = df['table_similarity'].std()
overall_std = df['overall_similarity'].std()

# Determine a more rigorous threshold using z-score
z_threshold = 2.0  # You can adjust this value as needed
threshold_title = title_avg - z_threshold * title_std
threshold_table = table_avg - z_threshold * table_std
threshold_overall = overall_avg - z_threshold * overall_std

# Get the 10 rows with the lowest title and table similarities
lowest_title_similarity = df.nsmallest(10, 'title_similarity')
lowest_table_similarity = df.nsmallest(10, 'table_similarity')

# Get the 10 rows with the highest title and table similarities
highest_title_similarity = df.nlargest(10, 'title_similarity')
highest_table_similarity = df.nlargest(10, 'table_similarity')

# Filter rows below the title similarity threshold with table similarity below 50%
below_threshold_df = df[(df['title_similarity'] < threshold_title) & (df['table_similarity'] < 50)]

# Save the filtered rows to a CSV file
below_threshold_df.to_csv('below_threshold.csv', index=False)

# Plotting the similarities using histograms
plt.figure(figsize=(12, 8))

# Histogram for title similarity
plt.hist(df['title_similarity'], bins=30, alpha=0.5, color='blue', label='Title Similarity')

# Histogram for table similarity
plt.hist(df['table_similarity'], bins=30, alpha=0.5, color='green', label='Table Similarity')

# Adding threshold lines
plt.axvline(x=threshold_title, color='blue', linestyle='--', label='Title Similarity Threshold')
plt.axvline(x=threshold_table, color='green', linestyle='--', label='Table Similarity Threshold')

# Adding titles and labels
plt.title('Distribution of Title and Table Similarity Scores with Thresholds')
plt.xlabel('Similarity Score')
plt.ylabel('Frequency')
plt.legend()

# Show the plot
plt.tight_layout()
plt.savefig('similarity_plot.png')
plt.show()

# Generate the stats.md file
with open('stats.md', 'w') as f:
    f.write("# Similarity Statistics\n\n")
    f.write("![Similarity Plot](similarity_plot.png)\n\n")
    f.write("## Statistics\n\n")
    f.write(
        f"\nAverage Title Similarity: {title_avg:.2f}\n"
        f"\nAverage Table Similarity: {table_avg:.2f}\n"
        f"\nAverage Overall Similarity: {overall_avg:.2f}\n"
        f"\nTitle Similarity Threshold (z={z_threshold}): {threshold_title:.2f}\n"
        f"\nTable Similarity Threshold (z={z_threshold}): {threshold_table:.2f}\n"
        f"\nOverall Similarity Threshold (z={z_threshold}): {threshold_overall:.2f}\n"
    )
    f.write("\n## 10 Rows with Lowest Title Similarity\n\n")
    f.write(lowest_title_similarity.to_markdown(index=False))
    f.write("\n\n## 10 Rows with Lowest Table Similarity\n\n")
    f.write(lowest_table_similarity.to_markdown(index=False))
    f.write("\n\n## 10 Rows with Highest Title Similarity\n\n")
    f.write(highest_title_similarity.to_markdown(index=False))
    f.write("\n\n## 10 Rows with Highest Table Similarity\n\n")
    f.write(highest_table_similarity.to_markdown(index=False))

# Part 2: Filter Instances Based on table_id
# Load the below_threshold.csv file
csv_file = 'below_threshold.csv'
df_below_threshold = pd.read_csv(csv_file)

# Get the list of table_ids from the CSV file
table_ids_below_threshold = df_below_threshold['table_id'].tolist()

# List of JSON files in the parent directory
json_files = ["../qtsumm_dev.json", "../qtsumm_test.json", "../qtsumm_train.json"]

# Initialize a list to hold all data from the JSON files
all_data = []

# Iterate through the JSON files and load the data
for json_file in json_files:
    with open(json_file, 'r') as f:
        data = json.load(f)
        all_data.extend(data)

# Filter the instances based on the table_id
filtered_instances_below_threshold = [instance for instance in all_data if instance['table']['table_id'] in table_ids_below_threshold]

# Save the filtered instances to a new JSON file
output_file_below_threshold = 'below_threshold_qtsumm.json'
with open(output_file_below_threshold, 'w') as f:
    json.dump(filtered_instances_below_threshold, f, indent=4)

print(f"Filtered {len(filtered_instances_below_threshold)} instances based on table_id and saved to {output_file_below_threshold}")

# Extract and save instances based on different criteria
def save_filtered_instances(instances, filename):
    with open(filename, 'w') as f:
        json.dump(instances, f, indent=4)

def get_filtered_instances(df, condition, json_data, top_n=10):
    table_ids = condition['table_id'].tolist()
    filtered = [instance for instance in json_data if instance['table']['table_id'] in table_ids]
    unique_tables = {}
    for instance in filtered:
        table_id = instance['table']['table_id']
        if table_id not in unique_tables:
            unique_tables[table_id] = instance
        if len(unique_tables) >= top_n:
            break
    return list(unique_tables.values())

# Get instances based on conditions
lowest_title_instances = get_filtered_instances(df, lowest_title_similarity, all_data)
lowest_table_instances = get_filtered_instances(df, lowest_table_similarity, all_data)
highest_title_instances = get_filtered_instances(df, highest_title_similarity, all_data)
highest_table_instances = get_filtered_instances(df, highest_table_similarity, all_data)

# Save instances to JSON files
save_filtered_instances(lowest_title_instances, 'lowest_title_similarity.json')
save_filtered_instances(lowest_table_instances, 'lowest_table_similarity.json')
save_filtered_instances(highest_title_instances, 'highest_title_similarity.json')
save_filtered_instances(highest_table_instances, 'highest_table_similarity.json')

print("Saved instances for different similarity criteria to respective JSON files.")
