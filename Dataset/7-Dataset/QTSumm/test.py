#pip install lxml


import json
import pandas as pd
import requests
from fuzzywuzzy import fuzz
from tqdm import tqdm
from bs4 import BeautifulSoup

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

def fetch_wikipedia_table(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        tables = soup.find_all('table', {'class': 'wikitable'})
        if tables:
            return pd.read_html(str(tables[0]), flavor='lxml')[0]
    except requests.RequestException as e:
        print(f"Request failed: {e}")
    except Exception as e:
        print(f"Error fetching table: {e}")
    return pd.DataFrame()

def extract_first_4x4(df):
    if not df.empty:
        df = df.astype(str)  # Ensure all data is string for fair comparison
        return df.iloc[:4, :4].fillna('')
    return pd.DataFrame()

def compare_tables(actual_df, matched_df):
    actual_sub = extract_first_4x4(actual_df)
    matched_sub = extract_first_4x4(matched_df)
    if actual_sub.empty or matched_sub.empty:
        return 0.0
    return fuzz.ratio(actual_sub.to_string(index=False, header=False), matched_sub.to_string(index=False, header=False))

def load_and_process_file(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
    
    output_data = []
    
    for item in tqdm(data, desc=f"Processing {filename}"):
        title = item['table']['title']
        table_id = item['table']['table_id']
        
        if 'rows' in item['table']:
            actual_table = pd.DataFrame(item['table']['rows'], columns=item['table']['header'])
        else:
            actual_table = pd.DataFrame()

        print(f"\nProcessing table: {title} with table_id: {table_id}")
        print(f"Actual table (first 4 rows and columns):\n{extract_first_4x4(actual_table)}\n")

        found_url, matched_title = search_wikipedia(title)
        print(f"Found URL: {found_url}, Matched Title: {matched_title}")
        
        similarity = fuzz.ratio(title.lower(), matched_title.lower()) if found_url != "Not found" else 0.0
        print(f"Title similarity: {similarity}")
        
        table_similarity = 0.0
        if found_url != "Not found":
            matched_table = fetch_wikipedia_table(found_url)
            print(f"Matched table (first 4 rows and columns):\n{extract_first_4x4(matched_table)}\n")
            table_similarity = compare_tables(actual_table, matched_table)
        
        print(f"Table similarity: {table_similarity}\n")
        
        output_data.append({
            "URL": found_url,
            "title": title,
            "table_id": table_id,
            "matched_title": matched_title,
            "title_similarity": similarity,
            "table_similarity": table_similarity
        })
        
    return output_data

def save_to_csv(data, filename):
    df = pd.DataFrame(data)
    csv_filename = filename.replace('.json', '.csv')
    df.to_csv(csv_filename, index=False)
    print(f"Saved data to {csv_filename}")

def main():
    for file_name in ['newdev.json']:
        data = load_and_process_file(file_name)
        save_to_csv(data, file_name)

if __name__ == "__main__":
    main()
