import requests
import csv
from tqdm import tqdm  # Import tqdm for the progress bar

def title_to_page_id(title):
    """Convert a Wikipedia page title to a page ID URL format."""
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "titles": title,
        "redirects": 1,  # Automatically resolve redirects
    }
    response = requests.get(url, params=params)
    data = response.json()
    page_id = next(iter(data['query']['pages']))
    return f"https://en.wikipedia.org/?curid={page_id}"

def convert_titles_to_page_ids(input_csv, output_csv):
    with open(input_csv, newline='', encoding='utf-8') as infile, \
         open(output_csv, 'w', newline='', encoding='utf-8') as outfile:
        reader = csv.DictReader(infile)
        # Prepare the output CSV file
        fieldnames = ['table_webpage_url', 'Page ID URL']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        
        # Convert to list for tqdm to be able to predict the total number of items
        rows = list(reader)
        for row in tqdm(rows, desc='Converting URLs', unit='url'):
            title_url = row['table_webpage_url']
            title = title_url.split('/')[-1]  # Extract the title part of the URL
            page_id_url = title_to_page_id(title.replace('_', ' '))
            writer.writerow({'table_webpage_url': title_url, 'Page ID URL': page_id_url})

# Example usage (adjust the paths as necessary)
convert_titles_to_page_ids('ToTTo-orignial-url.csv', 'Page_ID_URLs.csv')


