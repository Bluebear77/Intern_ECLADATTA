import csv
import matplotlib.pyplot as plt
from matplotlib_venn import venn2, venn3
import pandas as pd

def extract_curid(url):
    prefix = 'curid='
    start_index = url.find(prefix)
    if start_index != -1:
        start_index += len(prefix)
        return url[start_index:]
    return None

def read_urls(file_path, url_column):
    urls = set()
    with open(file_path, mode='r', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            curid = extract_curid(row[url_column])
            if curid:
                urls.add('http://en.wikipedia.org/?curid=' + curid)
    return urls

# File paths
fetaqa_file = 'FeTaQA_converted_urls.csv'
logicnlg_file = 'LOGICNLG-Original-URLs.csv'
lotnlg_file = 'LOTNLG-URLs.csv'
totto_file = 'ToTTo-Page-ID-URLs.csv'
report_file = 'Report.md'

# Read URLs from each file
fetaqa_urls = read_urls(fetaqa_file, 'converted_url')
logicnlg_urls = read_urls(logicnlg_file, 'URL')
lotnlg_urls = read_urls(lotnlg_file, 'URL')
totto_urls = read_urls(totto_file, 'Page ID URL')

# Collect sets
dataset_sets = [fetaqa_urls, logicnlg_urls, lotnlg_urls, totto_urls]
dataset_labels = ['FeTaQA', 'LOGICNLG', 'LOTNLG', 'ToTTo']

# Write the detailed statistical report to a Markdown file
with open(report_file, mode='w', encoding='utf-8') as mdfile:
    mdfile.write("# Detailed Statistical Report of Overlapped URLs\n\n")
    mdfile.write("## Individual Dataset Information\n\n")
    for label, urls in zip(dataset_labels, dataset_sets):
        mdfile.write(f"- **{label}**: {len(urls)} unique URLs\n")

    mdfile.write("\n## Overlaps Between Datasets\n\n")
    
    # Generate Venn diagrams and add them to the report
    for i in range(len(dataset_sets)):
        for j in range(i + 1, len(dataset_sets)):
            plt.figure()
            venn2([dataset_sets[i], dataset_sets[j]], set_labels=(dataset_labels[i], dataset_labels[j]))
            plt.title(f'Overlap between {dataset_labels[i]} and {dataset_labels[j]}')
            plt.savefig(f'venn_{i}_{j}.png')
            plt.close()
            mdfile.write(f"### {dataset_labels[i]} and {dataset_labels[j]}\n")
            mdfile.write(f"![Venn Diagram of {dataset_labels[i]} and {dataset_labels[j]}](venn_{i}_{j}.png)\n")
            mdfile.write(f"Total overlapping URLs: {len(dataset_sets[i] & dataset_sets[j])}\n\n")
            
    if len(dataset_sets) > 2:
        for i in range(len(dataset_sets)):
            for j in range(i + 1, len(dataset_sets)):
                for k in range(j + 1, len(dataset_sets)):
                    plt.figure()
                    venn3([dataset_sets[i], dataset_sets[j], dataset_sets[k]], set_labels=(dataset_labels[i], dataset_labels[j], dataset_labels[k]))
                    plt.title(f'Overlap among {dataset_labels[i]}, {dataset_labels[j]}, {dataset_labels[k]}')
                    plt.savefig(f'venn_{i}_{j}_{k}.png')
                    plt.close()
                    mdfile.write(f"### Overlap among {dataset_labels[i]}, {dataset_labels[j]}, {dataset_labels[k]}\n")
                    mdfile.write(f"![Venn Diagram](venn_{i}_{j}_{k}.png)\n")
                    mdfile.write(f"Total overlapping URLs: {len(dataset_sets[i] & dataset_sets[j] & dataset_sets[k])}\n\n")

    # Summary for four-way overlap
    if len(dataset_sets) == 4:
        all_overlap = dataset_sets[0] & dataset_sets[1] & dataset_sets[2] & dataset_sets[3]
        mdfile.write("## Summary for Four-Way Overlap\n")
        mdfile.write(f"All four datasets have {len(all_overlap)} common URLs.\n")
