import requests
import csv
from tqdm import tqdm  # Import tqdm for the progress bar

def page_id_to_title(page_id):
    """Convert a Wikipedia page ID to a title format URL."""
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "pageids": page_id,
    }
    response = requests.get(url, params=params)
    data = response.json()

    try:
        title = data['query']['pages'][page_id]['title']
        title_format_url = f"https://en.wikipedia.org/wiki/{title.replace(' ', '_')}"
        return title_format_url
    except KeyError:
        # If 'title' key is not found, return None to indicate failure
        return None

def convert_page_ids_to_titles(input_csv, output_csv, skipped_csv):
    with open(input_csv, newline='', encoding='utf-8') as infile, \
         open(output_csv, 'w', newline='', encoding='utf-8') as outfile, \
         open(skipped_csv, 'w', newline='', encoding='utf-8') as skippedfile:
        reader = csv.DictReader(infile)
        writer = csv.DictWriter(outfile, fieldnames=['URL', 'Title-Format URL'])
        skipped_writer = csv.DictWriter(skippedfile, fieldnames=['Skipped URL'])
        
        writer.writeheader()
        skipped_writer.writeheader()

        rows = list(reader)
        for row in tqdm(rows, desc='Converting Page IDs', unit='url'):
            page_id_url = row['URL']
            page_id = page_id_url.split('=')[-1]  # Extract the page ID from the URL
            title_format_url = page_id_to_title(page_id)
            
            if title_format_url:
                writer.writerow({'URL': page_id_url, 'Title-Format URL': title_format_url})
            else:
                # If conversion failed, write the URL to the skipped file
                skipped_writer.writerow({'Skipped URL': page_id_url})

# Example usage (adjust the paths as necessary)
convert_page_ids_to_titles('LOGICNLG-Original-URLs.csv', 'LOGICNLG-Title-Format-URLs.csv', 'LOGICNLG-Skipped-URLs.csv')
