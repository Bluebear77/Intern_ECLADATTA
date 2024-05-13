import json
import pandas as pd
import requests
from fuzzywuzzy import fuzz
from tqdm import tqdm

def search_wikipedia(title):
    base_url = "https://en.wikipedia.org/w/api.php"
    params = {
        'action': 'query',
        'list': 'search',
        'srsearch': title,
        'format': 'json'
    }
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # This will raise an exception for HTTP errors
        results = response.json().get('query', {}).get('search', [])
        if results:
            # Take the most relevant result
            top_result = results[0]
            page_id = top_result['pageid']
            url = f"http://en.wikipedia.org/?curid={page_id}"
            return url, top_result['title']
    except requests.RequestException as e:
        print(f"Request failed: {e}")
    except json.JSONDecodeError:
        print("Failed to decode JSON from response.")
    return "Not found", "No title matched"

def load_and_process_file(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
    
    output_data = []
    
    for item in tqdm(data, desc=f"Processing {filename}"):
        title = item['table']['title']
        table_id = item['table']['table_id']
        found_url, matched_title = search_wikipedia(title)
        similarity = fuzz.ratio(title.lower(), matched_title.lower()) if found_url != "Not found" else 0.0
        
        output_data.append({
            "URL": found_url,
            "title": title,
            "table_id": table_id,
            "matched_title": matched_title,
            "similarity": similarity
        })
        
    return output_data

def save_to_csv(data, filename):
    df = pd.DataFrame(data)
    csv_filename = filename.replace('.json', '.csv')
    df.to_csv(csv_filename, index=False)
    print(f"Saved data to {csv_filename}")

def main():
    for file_name in ['qtsumm_dev.json', 'qtsumm_test.json', 'qtsumm_train.json']:
        data = load_and_process_file(file_name)
        save_to_csv(data, file_name)

if __name__ == "__main__":
    main()
