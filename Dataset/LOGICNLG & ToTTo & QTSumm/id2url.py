import json
import csv

# Load JSON data
with open('LOGICNLG-ids.json', 'r') as file:
    table_ids = json.load(file)

# Open a CSV file to write the URLs
with open('table_urls.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['URL'])  # Column header

    for id in table_ids:
        # Extract the page ID part from the file name
        page_id = id.split('-')[1]
        # Create the URL
        url = f"http://en.wikipedia.org/?curid={page_id}"
        # Write the URL to the CSV file
        writer.writerow([url])
