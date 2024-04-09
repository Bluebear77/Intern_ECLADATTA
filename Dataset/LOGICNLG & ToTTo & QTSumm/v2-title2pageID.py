import requests
import csv
from tqdm import tqdm  # Import tqdm for the progress bar

def title_to_page_id(title):
    # Replace spaces with underscores for the API request
    title = title.replace(' ', '_')
    # Construct the query URL for the Wikipedia API
    api_url = f"https://en.wikipedia.org/w/api.php?action=query&prop=pageprops&titles={title}&format=json"
    try:
        # Send a request to the Wikipedia API
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an HTTPError for bad responses

        # Parse the JSON response
        data = response.json()
        
        # Extract the page ID from the JSON response
        pages = data.get("query", {}).get("pages", {})
        page_id = next(iter(pages.keys()))  # Get the first key in the 'pages' dictionary
        if page_id == "-1":
            return "Page not found"
        
        # Construct the page ID format URL
        page_id_format_url = f"http://en.wikipedia.org/?curid={page_id}"
        return page_id_format_url
    except requests.RequestException as e:
        return f"Error: {e}"

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
            # Extract the title part of the URL, assuming it's the last part after '/'
            title = title_url.split('/')[-1]
            # Convert title to Page ID URL
            page_id_url = title_to_page_id(title)
            # Write the result to the output CSV file
            writer.writerow({'table_webpage_url': title_url, 'Page ID URL': page_id_url})

# Example usage (adjust the paths as necessary)
# Note: Make sure the CSV file 'ToTTo-Orignial-URLs.csv' exists and has the correct format before running this.
convert_titles_to_page_ids('ToTTo-Invalid-Page-ID-URLs.csv', 'ToTTo-Fixed-Invalid-Page-ID-URLs.csv')
