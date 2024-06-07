import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm
import numpy as np

# Load the data from the CSV file
input_file = 'qtsumm_complete_v1.csv'
df = pd.read_csv(input_file)

# Calculate statistics
title_avg = df['title_similarity'].mean()
table_avg = df['table_similarity'].mean()
overall_avg = df['overall_similarity'].mean()

title_std = df['title_similarity'].std()
table_std = df['table_similarity'].std()
overall_std = df['overall_similarity'].std()

# Determine a more rigorous threshold using z-score
z_threshold = 1.0  # You can adjust this value as needed
threshold_title = title_avg - z_threshold * title_std
threshold_table = table_avg - z_threshold * table_std
threshold_overall = overall_avg - z_threshold * overall_std

# Output the statistics to a text file
stats_content = (
    f"Average Title Similarity: {title_avg:.2f}\n"
    f"Average Table Similarity: {table_avg:.2f}\n"
    f"Average Overall Similarity: {overall_avg:.2f}\n"
    f"Title Similarity Threshold (z={z_threshold}): {threshold_title:.2f}\n"
    f"Table Similarity Threshold (z={z_threshold}): {threshold_table:.2f}\n"
    f"Overall Similarity Threshold (z={z_threshold}): {threshold_overall:.2f}\n"
    "\nTables below these thresholds should not be considered.\n"
)

with open('stats.txt', 'w') as f:
    f.write(stats_content)

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
    f.write(stats_content)
