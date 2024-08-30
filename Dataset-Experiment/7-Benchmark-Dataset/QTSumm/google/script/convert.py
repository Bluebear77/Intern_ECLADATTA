import csv
import requests

def get_curid_from_url(url):
    if "curid=" in url:
        return url  # Already in the desired format
    else:
        # Extract page name from URL
        page_name = url.split("/wiki/")[-1]
        
        # Fetch page ID using Wikipedia API
        api_url = f"https://en.wikipedia.org/w/api.php?action=query&titles={page_name}&format=json"
        response = requests.get(api_url)
        data = response.json()
        
        page_id = list(data['query']['pages'].keys())[0]
        
        if page_id != "-1":  # -1 indicates page not found
            return f"http://en.wikipedia.org/?curid={page_id}"
        else:
            return url

def process_csv(input_file, output_file):
    with open(input_file, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        rows = list(reader)
        
    for row in rows:
        row['URL'] = get_curid_from_url(row['URL'])
    
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = reader.fieldnames
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        writer.writerows(rows)

# Example usage
input_file = 'test.csv'
output_file = f"{input_file.rsplit('.', 1)[0]}-d.csv"
process_csv(input_file, output_file)

