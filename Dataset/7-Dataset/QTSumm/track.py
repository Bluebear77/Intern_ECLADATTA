
import json
import csv
import requests
from tqdm import tqdm
from difflib import SequenceMatcher

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def find_wikipedia_url(title):
    # URL to the Wikipedia search API
    api_url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "list": "search",
        "srsearch": title,
        "srlimit": 5  # Retrieve top 5 results to increase the chance of finding a relevant match
    }
    response = requests.get(api_url, params=params)
    data = response.json()
    
    if data['query']['search']:
        for result in data['query']['search']:
            result_title = result['title']
            similarity_score = similar(title.lower(), result_title.lower()) * 100  # Calculating similarity as a percentage
            if similarity_score >= 80:  # Check if the similarity is above the threshold
                page_id = result['pageid']
                return f"http://en.wikipedia.org/?curid={page_id}", result_title, similarity_score
    return "Not found", "No title matched", 0.0  # Return 'Not found' if no suitable match is found

def process_file(filename):
    output_filename = filename.replace(".json", ".csv")
    with open(filename, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    with open(output_filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['URL', 'title', 'table_id', 'matched_title', 'similarity']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for entry in tqdm(data, desc=f"Processing {filename}"):
            title = entry['table']['title']
            table_id = entry['table']['table_id']
            url, matched_title, similarity_score = find_wikipedia_url(title)
            writer.writerow({'URL': url, 'title': title, 'table_id': table_id, 'matched_title': matched_title, 'similarity': similarity_score})

def main():
    files = ['qtsumm_dev.json', 'qtsumm_test.json', 'qtsumm_train.json']
    for file in files:
        process_file(file)

if __name__ == "__main__":
    main()
