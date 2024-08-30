import os
import pandas as pd
import matplotlib.pyplot as plt

# List of datasets with before and after cleaning filenames
datasets = [
    ('F2WTQ', 'F2WTQ.csv', 'F2WTQ-cleaned.csv'),
    ('FeTaQA', 'FeTaQA.csv', 'FeTaQA-cleaned.csv'),
    ('LOGICNLG', 'LOGICNLG.csv', 'LOGICNLG-cleaned.csv'),
    ('LOTNLG', 'LOTNLG.csv', 'LOTNLG-cleaned.csv'),
    ('ToTTo', 'ToTTo.csv', 'ToTTo-cleaned.csv'),
    ('WTQ', 'WTQ.csv', 'WTQ-cleaned.csv'),
    ('telco100', 'telco100.csv', 'telco100.csv'),
    ('business100', 'business100.csv', 'business100.csv'),
    ('female100', 'female100.csv', 'female100.csv'),
    ('female100_english', 'female100_english.csv', 'female100_english.csv')
]

# Initialize lists to store data for plotting
dataset_names = []
all_urls_count = []
unique_urls_count = []

# Iterate over each dataset to calculate the counts
for dataset_name, all_file, cleaned_file in datasets:
    # Read the original and cleaned CSV files
    all_urls = pd.read_csv(all_file)
    cleaned_urls = pd.read_csv(cleaned_file)
    
    # Count the number of URLs
    all_count = len(all_urls)
    cleaned_count = len(cleaned_urls)
    
    # Store the dataset name and counts
    dataset_names.append(dataset_name)
    all_urls_count.append(all_count)
    unique_urls_count.append(cleaned_count)

# Create a bar chart
x = range(len(dataset_names))
width = 0.35  # Width of the bars

plt.figure(figsize=(12, 8))
plt.bar(x, all_urls_count, width, label='Total URLs', color='blue')
plt.bar([i + width for i in x], unique_urls_count, width, label='Unique URLs', color='orange')

# Add labels and title
plt.xlabel('Dataset')
plt.ylabel('Number of URLs (Log Scale)')
plt.yscale('log')
plt.title('Comparison of Total URLs vs Unique URLs After Cleaning')
plt.xticks([i + width/2 for i in x], dataset_names, rotation=45, ha="right")
plt.legend()

# Save the plot as a PNG file in the current directory
plt.tight_layout()
plt.savefig('url_comparison_chart_log_scale.png')
