import csv
import matplotlib.pyplot as plt
import pandas as pd
from upsetplot import plot, from_contents

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

# Collect sets for upset plot
dataset_sets = {
    'FeTaQA': fetaqa_urls,
    'LOGICNLG': logicnlg_urls,
    'LOTNLG': lotnlg_urls,
    'ToTTo': totto_urls
}

# Calculate overlaps for pairs
pairs = [
    ("FeTaQA", "LOGICNLG", fetaqa_urls & logicnlg_urls),
    ("FeTaQA", "LOTNLG", fetaqa_urls & lotnlg_urls),
    ("FeTaQA", "ToTTo", fetaqa_urls & totto_urls),
    ("LOGICNLG", "LOTNLG", logicnlg_urls & lotnlg_urls),
    ("LOGICNLG", "ToTTo", logicnlg_urls & totto_urls),
    ("LOTNLG", "ToTTo", lotnlg_urls & totto_urls)
]

# Write the detailed statistical report to a Markdown file
with open(report_file, mode='w', encoding='utf-8') as mdfile:
    mdfile.write("# Detailed Statistical Report of Overlapped URLs\n\n")
    mdfile.write("## Overlaps Between Datasets\n\n")
    for (set1, set2, intersection) in pairs:
        mdfile.write(f"### {set1} and {set2}\n")
        mdfile.write(f"Total overlapping URLs: {len(intersection)}\n\n")

# Prepare and plot the data using upsetplot
upset_data = from_contents(dataset_sets)
plot(upset_data, orientation='horizontal')
plt.title('UpSet Plot of Dataset Overlaps')
plt.savefig('upset_plot.png')
plt.show()

# Append plot image to Markdown report
with open(report_file, 'a', encoding='utf-8') as mdfile:
    mdfile.write("## UpSet Plot of Dataset Overlaps\n")
    mdfile.write("![UpSet Plot of Dataset Overlaps](upset_plot.png)\n")
