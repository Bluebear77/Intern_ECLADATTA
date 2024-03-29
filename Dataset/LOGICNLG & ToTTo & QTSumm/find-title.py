import csv

# Define the input file name
input_csv = 'Comparision-LOGICNLG-Title-ToTTo.csv'
# Define the output file name for overlapped URLs
output_csv = 'Overlapped-URLs.csv'

# Initialize sets to store URLs from both columns
logicnlg_urls = set()
totto_urls = set()

# Read the input CSV and populate the sets
with open(input_csv, mode='r', encoding='utf-8') as infile:
    reader = csv.DictReader(infile)
    for row in reader:
        logicnlg_urls.add(row['LOGICNLG-Title-Format-URLs'].strip().lower())
        totto_urls.add(row['ToTTo-Orignial-URLs'].strip().lower())

# Find overlap between the two sets
overlapped_urls = logicnlg_urls.intersection(totto_urls)

# If there are overlapped URLs, write them to the output CSV
if overlapped_urls:
    with open(output_csv, mode='w', encoding='utf-8', newline='') as outfile:
        writer = csv.writer(outfile)
        # Write the header
        writer.writerow(['Overlapped URLs'])
        # Write each overlapped URL
        for url in overlapped_urls:
            writer.writerow([url])
    print(f"Overlapped URLs written to {output_csv}")
else:
    print("No overlapped URLs found.")
