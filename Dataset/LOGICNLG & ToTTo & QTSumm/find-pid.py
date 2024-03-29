import csv

# File paths
logicnlg_file = 'LOGICNLG-Original-URLs.csv'
totto_file = 'ToTTo-Page-ID-URLs.csv'
output_file = 'Overlapped-URLs.csv'

# Function to extract curid from URL
def extract_curid(url):
    prefix = 'curid='
    start_index = url.find(prefix)
    if start_index != -1:
        start_index += len(prefix)
        return url[start_index:]
    return None

# Read LOGICNLG URLs and store their page IDs and URLs
logicnlg_urls = {}
with open(logicnlg_file, mode='r', encoding='utf-8') as infile:
    reader = csv.reader(infile)
    next(reader)  # Skip the header
    for row in reader:
        curid = extract_curid(row[0])
        if curid:
            logicnlg_urls[curid] = row[0]

# Prepare a dictionary to store overlapped page IDs with both URLs
overlapped_info = {}

# Check ToTTo URLs for overlaps and store relevant data
with open(totto_file, mode='r', encoding='utf-8') as infile:
    reader = csv.DictReader(infile)
    for row in reader:
        curid = extract_curid(row['Page ID URL'])
        if curid and curid in logicnlg_urls:
            overlapped_info[curid] = {'LOGICNLG_URL': logicnlg_urls[curid], 'ToTTo_URL': row['table_webpage_url']}

# Write overlapped info to the output file
if overlapped_info:
    with open(output_file, mode='w', encoding='utf-8', newline='') as outfile:
        writer = csv.writer(outfile)
        # Write the header
        writer.writerow(['Page ID', 'LOGICNLG URL', 'ToTTo URL'])
        # Write each overlapped page ID with its URLs
        for curid, urls in overlapped_info.items():
            writer.writerow([curid, urls['LOGICNLG_URL'], urls['ToTTo_URL']])
    print(f"Overlapped page IDs and URLs written to {output_file}")
else:
    print("No overlapped page IDs found.")
