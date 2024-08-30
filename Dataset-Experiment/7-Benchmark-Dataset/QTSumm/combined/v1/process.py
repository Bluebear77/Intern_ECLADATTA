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

# Determine thresholds using z-scores for z=1.0 and z=2.0
z_scores = [1.0, 2.0]
thresholds = {}

for z in z_scores:
    thresholds[z] = {
        'title': title_avg - z * title_std,
        'table': table_avg - z * table_std,
        'overall': overall_avg - z * overall_std
    }

# Get the 5 rows with the lowest and highest title and table similarities
lowest_title_similarity = df.nsmallest(5, 'title_similarity')
lowest_table_similarity = df.nsmallest(5, 'table_similarity')
highest_title_similarity = df.nlargest(5, 'title_similarity')
highest_table_similarity = df.nlargest(5, 'table_similarity')

# Filter rows below the title similarity threshold with table similarity below 50% for z=1.0 and z=2.0
below_threshold_dfs = {}

for z in z_scores:
    below_threshold_dfs[z] = df[(df['title_similarity'] < thresholds[z]['title']) & (df['table_similarity'] < 50)]

# Save the filtered rows to CSV files
for z in z_scores:
    below_threshold_dfs[z].to_csv(f'below_threshold_z_{z}.csv', index=False)

# Plotting the similarities using histograms
for z in z_scores:
    plt.figure(figsize=(12, 8))
    plt.hist(df['title_similarity'], bins=30, alpha=0.5, color='blue', label='Title Similarity')
    plt.hist(df['table_similarity'], bins=30, alpha=0.5, color='green', label='Table Similarity')
    plt.axvline(x=thresholds[z]['title'], color='blue', linestyle='--', label=f'Title Similarity Threshold (z={z})')
    plt.axvline(x=thresholds[z]['table'], color='green', linestyle='--', label=f'Table Similarity Threshold (z={z})')
    plt.title(f'Distribution of Title and Table Similarity Scores with Thresholds (z={z})')
    plt.xlabel('Similarity Score')
    plt.ylabel('Frequency')
    plt.legend()
    plt.tight_layout()
    plt.savefig(f'similarity_plot_z_{z}.png')
    plt.show()

# Generate the stats.md file
with open('stats.md', 'w') as f:
    f.write("# Similarity Statistics\n\n")
    for z in z_scores:
        f.write(f"![Similarity Plot (z={z})](similarity_plot_z_{z}.png)\n\n")
    f.write("## Statistics\n\n")
    f.write(f"\nAverage Title Similarity: {title_avg:.2f}\n")
    f.write(f"\nAverage Table Similarity: {table_avg:.2f}\n")
    f.write(f"\nAverage Overall Similarity: {overall_avg:.2f}\n")
    for z in z_scores:
        f.write(f"\nTitle Similarity Threshold (z={z}): {thresholds[z]['title']:.2f}\n")
        f.write(f"\nTable Similarity Threshold (z={z}): {thresholds[z]['table']:.2f}\n")
        f.write(f"\nOverall Similarity Threshold (z={z}): {thresholds[z]['overall']:.2f}\n")
    f.write("\n## 5 Rows with Lowest Title Similarity\n\n")
    f.write(lowest_title_similarity.to_markdown(index=False))
    f.write("\n\n## 5 Rows with Lowest Table Similarity\n\n")
    f.write(lowest_table_similarity.to_markdown(index=False))
    f.write("\n\n## 5 Rows with Highest Title Similarity\n\n")
    f.write(highest_title_similarity.to_markdown(index=False))
    f.write("\n\n## 5 Rows with Highest Table Similarity\n\n")
    f.write(highest_table_similarity.to_markdown(index=False))

# Part 2: Filter Instances Based on table_id
# Load the below_threshold.csv files for z=1.0 and z=2.0
below_threshold_files = {z: f'below_threshold_z_{z}.csv' for z in z_scores}
df_below_thresholds = {z: pd.read_csv(below_threshold_files[z]) for z in z_scores}

# Get the list of table_ids from the CSV files
table_ids_below_thresholds = {z: df_below_thresholds[z]['table_id'].tolist() for z in z_scores}

# List of JSON files in the parent directory
json_files = ["../../qtsumm_dev.json", "../../qtsumm_test.json", "../../qtsumm_train.json"]

# Initialize a list to hold all data from the JSON files
all_data = []

# Iterate through the JSON files and load the data
for json_file in json_files:
    with open(json_file, 'r') as f:
        data = json.load(f)
        all_data.extend(data)

# Filter the instances based on the table_id for z=1.0 and z=2.0
filtered_instances_below_thresholds = {z: [instance for instance in all_data if instance['table']['table_id'] in table_ids_below_thresholds[z]] for z in z_scores}

# Save the filtered instances to new JSON files
for z in z_scores:
    output_file_below_threshold = f'below_threshold_qtsumm_z_{z}.json'
    with open(output_file_below_threshold, 'w') as f:
        json.dump(filtered_instances_below_thresholds[z], f, indent=4)
    print(f"Filtered {len(filtered_instances_below_thresholds[z])} instances based on table_id and saved to {output_file_below_threshold}")

# Extract and save instances based on different criteria
def save_filtered_instances(instances, filename):
    with open(filename, 'w') as f:
        json.dump(instances, f, indent=4)

def get_filtered_instances(df, condition, json_data, top_n=5):
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
