import csv
import matplotlib.pyplot as plt

# File paths
fetaqa_file = 'FeTaQA_converted_urls.csv'
logicnlg_file = 'LOGICNLG-Original-URLs.csv'
lotnlg_file = 'LOTNLG-URLs.csv'
totto_file = 'ToTTo-Page-ID-URLs.csv'
output_file = 'Overlapped-URLs.csv'
report_file = 'Report.md'

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

# Read URLs from each file
fetaqa_urls = read_urls(fetaqa_file, 'converted_url')
logicnlg_urls = read_urls(logicnlg_file, 'URL')
lotnlg_urls = read_urls(lotnlg_file, 'URL')
totto_urls = read_urls(totto_file, 'Page ID URL')

# Prepare a set for all unique URLs and a dictionary to count occurrences
all_urls = fetaqa_urls.union(logicnlg_urls, lotnlg_urls, totto_urls)
url_counts = {url: sum(url in urls for urls in [fetaqa_urls, logicnlg_urls, lotnlg_urls, totto_urls]) for url in all_urls}

# Filter URLs that appear in more than one file
overlapped_urls = {url for url, count in url_counts.items() if count > 1}

# Write overlapped URLs to the output file
with open(output_file, mode='w', encoding='utf-8', newline='') as outfile:
    writer = csv.writer(outfile)
    writer.writerow(['URL'])
    for url in overlapped_urls:
        writer.writerow([url])

# Generate and save a graph
file_counts = [len(fetaqa_urls), len(logicnlg_urls), len(lotnlg_urls), len(totto_urls)]
file_names = ['FeTaQA', 'LOGICNLG', 'LOTNLG', 'ToTTo']
plt.figure(figsize=(10, 6))
plt.bar(file_names, file_counts, color=['blue', 'green', 'red', 'purple'])
plt.title('URLs in Each File')
plt.ylabel('Number of URLs')
plt.savefig('urls_in_each_file.png')

# Write the detailed statistical report to a Markdown file
with open(report_file, mode='w', encoding='utf-8') as mdfile:
    mdfile.write("# Detailed Statistical Report of Overlapped URLs\n\n")
    mdfile.write(f"Total unique URLs considered: {len(all_urls)}\n")
    mdfile.write(f"Total URLs from FeTaQA: {len(fetaqa_urls)}\n")
    mdfile.write(f"Total URLs from LOGICNLG: {len(logicnlg_urls)}\n")
    mdfile.write(f"Total URLs from LOTNLG: {len(lotnlg_urls)}\n")
    mdfile.write(f"Total URLs from ToTTo: {len(totto_urls)}\n")
    mdfile.write(f"Total overlapped URLs across files: {len(overlapped_urls)}\n\n")
    mdfile.write("## URLs in Each File Graph\n")
    mdfile.write("![URLs in Each File](urls_in_each_file.png)\n")
