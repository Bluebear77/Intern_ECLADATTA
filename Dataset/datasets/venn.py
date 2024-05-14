import pandas as pd
import matplotlib.pyplot as plt
from matplotlib_venn import venn2
import os

# List of dataset filenames
datasets = [
    "F2WTQ.csv", "FeTaQA.csv", "LOGICNLG.csv", "LOTNLG.csv", "ToTTo.csv",
    "WTQ.csv", "business100.csv", "female100.csv", "telco100.csv", "female100_english.csv"
]

# Dictionary to store URLs from each dataset
url_dict = {}

# Load datasets and extract URLs
for dataset in datasets:
    df = pd.read_csv(dataset)
    url_dict[dataset] = set(df.iloc[:, 0])

# Pairs to visualize, including the new pair
pairs = [
    ("LOGICNLG.csv", "LOTNLG.csv"),
    ("F2WTQ.csv", "WTQ.csv"),
    ("LOGICNLG.csv", "ToTTo.csv"),
    ("LOTNLG.csv", "ToTTo.csv"),
    ("ToTTo.csv", "telco100.csv"),
    ("ToTTo.csv", "business100.csv"),
    ("female100_english.csv", "ToTTo.csv")  # New pair added here
]

# Function to plot and save Venn diagrams for given pairs
def plot_venn(pair, url_dict):
    set1 = url_dict[pair[0]]
    set2 = url_dict[pair[1]]
    venn2([set1, set2], set_labels=(pair[0], pair[1]))
    plt.title(f"Venn Diagram: {pair[0]} & {pair[1]}")
    output_filename = f"venn_{pair[0].split('.')[0]}_{pair[1].split('.')[0]}.png"
    plt.savefig(output_filename)
    plt.close()

# Generate and save Venn diagrams for each pair
for pair in pairs:
    plot_venn(pair, url_dict)

# Result summary and explanation
def interpret_overlap(url_dict, pairs):
    total_urls = {url for urls in url_dict.values() for url in urls}
    print(f"Total unique URLs across all datasets: {len(total_urls)}")

    overlap_info = {}
    for dataset1, dataset2 in pairs:
        overlap = len(url_dict[dataset1] & url_dict[dataset2])
        overlap_info[(dataset1, dataset2)] = overlap

    sorted_overlap_info = sorted(overlap_info.items(), key=lambda x: x[1], reverse=True)
    print("\nPairwise dataset overlap counts:")
    for (ds1, ds2), count in sorted_overlap_info:
        print(f"{ds1} & {ds2}: {count}")

    # Find datasets with highest overlap
    most_overlapping_datasets = sorted_overlap_info[0]
    print(f"\nDatasets with the highest overlap: {most_overlapping_datasets[0][0]} & {most_overlapping_datasets[0][1]} ({most_overlapping_datasets[1]} URLs)")

interpret_overlap(url_dict, pairs)
