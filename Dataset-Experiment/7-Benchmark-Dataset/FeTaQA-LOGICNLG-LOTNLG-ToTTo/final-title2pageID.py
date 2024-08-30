import requests
import csv
from urllib.parse import unquote
from tqdm import tqdm

def get_wikipedia_page_id(title):
    # Properly encode special characters in the title
    title = unquote(title)  # Decode percent-encoded characters
    params = {
        'action': 'query',
        'prop': 'pageprops',
        'titles': title,
        'format': 'json'
    }
    api_url = "https://en.wikipedia.org/w/api.php"
    
    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()
        data = response.json()
        
        pages = data.get('query', {}).get('pages', {})
        page_id = next(iter(pages.keys()))
        
        if page_id == "-1":
            return "Page not found"
        else:
            return f"http://en.wikipedia.org/?curid={page_id}"
    except requests.RequestException as e:
        return f"Error: {e}"

def convert_urls_to_page_ids(input_csv, output_csv):
    successful_count = 0
    failed_count = 0
    
    with open(input_csv, newline='', encoding='utf-8') as infile, \
         open(output_csv, 'w', newline='', encoding='utf-8') as outfile:
        
        reader = csv.DictReader(infile)
        writer = csv.DictWriter(outfile, fieldnames=['table_webpage_url', 'Page ID URL'])
        writer.writeheader()

        # Convert to list for tqdm to be able to predict the total number of items
        rows = list(reader)
        for row in tqdm(rows, desc='Converting URLs', unit='url'):
            title_url = row['table_webpage_url']
            # Extract the title part of the URL, assuming it's the last part after '/'
            title = title_url.split('/wiki/')[-1]
            page_id_url = get_wikipedia_page_id(title)
            if page_id_url.startswith("http://en.wikipedia.org/?curid="):
                successful_count += 1
            else:
                failed_count += 1
            writer.writerow({'table_webpage_url': title_url, 'Page ID URL': page_id_url})

    return successful_count, failed_count

# Paths to your input and output CSV files
input_csv_path = 'ToTTo-Invalid-Page-ID-URLs.csv'
output_csv_path = 'output_fixed.csv'

successful_count, failed_count = convert_urls_to_page_ids(input_csv_path, output_csv_path)
print(f"Successful conversions: {successful_count}")
print(f"Failed conversions: {failed_count}")
