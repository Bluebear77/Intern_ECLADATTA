import pandas as pd
import matplotlib.pyplot as plt
from upsetplot import UpSet, from_contents
import warnings

# Suppress future warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# List of dataset filenames
datasets = [
    "F2WTQ.csv", "FeTaQA.csv", "LOGICNLG.csv", "LOTNLG.csv", "ToTTo.csv",
    "WTQ.csv", "business100.csv", "female100.csv", "telco100.csv","female100_english.csv"
]

# Dictionary to store URLs from each dataset
url_dict = {}

# Load datasets and extract URLs
for dataset in datasets:
    df = pd.read_csv(dataset)
    url_dict[dataset] = set(df.iloc[:, 0])

# Prepare data for the UpSet plot
contents = {name: list(urls) for name, urls in url_dict.items()}

# Create an UpSet plot
upset_data = from_contents(contents)
upset = UpSet(upset_data)

# Plot the UpSet plot
upset.plot()
plt.suptitle('URL Overlap Across Datasets')

# Save the plot as a PNG file
plt.savefig('upset_plot.png', dpi=300)

# Interpretation of the result written to stats.md
def interpret_overlap(url_dict):
    with open('stats.md', 'w') as file:
        total_urls = {url for urls in url_dict.values() for url in urls}
        file.write(f"Total unique URLs across all datasets: {len(total_urls)}\n")

        overlap_info = {}
        for dataset1, urls1 in url_dict.items():
            for dataset2, urls2 in url_dict.items():
                if dataset1 != dataset2:
                    overlap = len(urls1 & urls2)
                    key = tuple(sorted([dataset1, dataset2]))
                    if key not in overlap_info:
                        overlap_info[key] = overlap

        sorted_overlap_info = sorted(overlap_info.items(), key=lambda x: x[1], reverse=True)
        file.write("\nPairwise dataset overlap counts:\n")
        for (ds1, ds2), count in sorted_overlap_info:
            file.write(f"{ds1} & {ds2}: {count}\n")

        # Find datasets with highest overlap
        most_overlapping_datasets = sorted_overlap_info[0]
        file.write(f"\nDatasets with the highest overlap: {most_overlapping_datasets[0][0]} & {most_overlapping_datasets[0][1]} ({most_overlapping_datasets[1]} URLs)\n")

interpret_overlap(url_dict)

# --- Additional Section for Bar Plots ---

# Number of URLs in each dataset (non-unique)
url_counts = {}
for dataset in datasets:
    df = pd.read_csv(dataset)
    url_counts[dataset] = len(df.iloc[:, 0])

# Unique URL counts
unique_url_counts = {dataset: len(urls) for dataset, urls in url_dict.items()}

# 1. Bar plot indicating the URL number of each dataset
plt.figure(figsize=(12, 6))  # Increase the figure size for more space
plt.bar(url_counts.keys(), url_counts.values())
plt.title("Number of URLs in Each Dataset")
plt.xlabel("Dataset")
plt.ylabel("Number of URLs")
plt.xticks(rotation=45, ha='right')

# Adding the number above each bar with smaller font size
for i, count in enumerate(url_counts.values()):
    plt.text(i, count, str(count), ha='center', va='bottom', fontsize=8)  # Reduced font size to avoid overlapping

plt.tight_layout()
plt.savefig('url_counts_per_dataset.png', dpi=300)
plt.show()

# 2. Bar plot comparing URL number and unique URL number for each dataset
plt.figure(figsize=(12, 6))  # Increase the figure size for more space

# Bar positions
positions = range(len(datasets))
bar_width = 0.35  # Reduced the bar width for better spacing

# Plotting both bars side by side for each dataset
plt.bar([p - bar_width/2 for p in positions], url_counts.values(), width=bar_width, label='Total URLs')
plt.bar([p + bar_width/2 for p in positions], unique_url_counts.values(), width=bar_width, label='Unique URLs')

plt.title("Comparison of Total URLs and Unique URLs per Dataset")
plt.xlabel("Dataset")
plt.ylabel("Number of URLs")
plt.xticks(positions, datasets, rotation=45, ha='right')

# Adding the number above each bar with smaller font size
for i, (total_count, unique_count) in enumerate(zip(url_counts.values(), unique_url_counts.values())):
    plt.text(i - bar_width/2, total_count, str(total_count), ha='center', va='bottom', fontsize=8)  # Reduced font size
    plt.text(i + bar_width/2, unique_count, str(unique_count), ha='center', va='bottom', fontsize=8)  # Reduced font size

plt.legend()
plt.tight_layout()
plt.savefig('comparison_url_counts.png', dpi=300)
plt.show()
