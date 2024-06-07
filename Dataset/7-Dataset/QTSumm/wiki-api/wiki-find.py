import subprocess
import sys
import time
from urllib.parse import urlparse, parse_qs
import random
from io import StringIO

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# List of packages to ensure are installed
required_packages = [
    "pandas",
    "requests",
    "fuzzywuzzy",
    "tqdm",
    "beautifulsoup4",
    "lxml"
]

for package in required_packages:
    try:
        __import__(package)
    except ImportError:
        install(package)


import json
import pandas as pd
import requests
from fuzzywuzzy import fuzz
from tqdm import tqdm
from bs4 import BeautifulSoup
from io import StringIO
import logging

# Ensure necessary packages are installed
# pip install lxml
# pip install tqdm
# pip install fuzzywuzzy

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger()

# Create file handler to log to a file
file_handler = logging.FileHandler('log.txt')
file_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

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
        logger.info(f"Request failed: {e}")
    except json.JSONDecodeError:
        logger.info("Failed to decode JSON from response.")
    return "Not found", "No title matched"

def fetch_all_wikipedia_tables(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        tables = soup.find_all('table', {'class': 'wikitable'})
        dataframes = [pd.read_html(StringIO(str(table)), flavor='lxml')[0] for table in tables]
        return dataframes
    except requests.RequestException as e:
        logger.info(f"Request failed: {e}")
    except Exception as e:
        logger.info(f"Error fetching tables: {e}")
    return []

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

def find_most_similar_table(url, input_df):
    extracted_tables = fetch_all_wikipedia_tables(url)
    highest_score = 0
    most_similar_table = pd.DataFrame()

    for table in extracted_tables:
        score = compare_tables(input_df, table)
        if score > highest_score:
            highest_score = score
            most_similar_table = table

    return most_similar_table, highest_score

def load_and_process_file(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
    
    output_data = []
    highest_overall_similarity = 0
    best_url = "Not found"
    best_matched_table = pd.DataFrame()
    
    for item in tqdm(data, desc=f"Processing {filename}"):
        title = item['table']['title']
        table_id = item['table']['table_id']
        
        if 'rows' in item['table']:
            actual_table = pd.DataFrame(item['table']['rows'], columns=item['table']['header'])
        else:
            actual_table = pd.DataFrame()

        logger.info(f"\nProcessing table: {title} with table_id: {table_id}")
        logger.info(f"Actual table (first 4 rows and columns):\n{extract_first_4x4(actual_table)}\n")

        found_url, matched_title = search_wikipedia(title)
        logger.info(f"Found URL: {found_url}, Matched Title: {matched_title}")
        
        title_similarity = fuzz.ratio(title.lower(), matched_title.lower()) if found_url != "Not found" else 0.0
        logger.info(f"Title similarity: {title_similarity}")
        
        table_similarity = 0.0
        most_similar_table = pd.DataFrame()
        if found_url != "Not found":
            most_similar_table, table_similarity = find_most_similar_table(found_url, actual_table)
            logger.info(f"Most similar table (first 4 rows and columns):\n{extract_first_4x4(most_similar_table)}\n")
        
        logger.info(f"Table similarity: {table_similarity}\n")
        
        overall_similarity = int(0.7 * title_similarity + 0.3 * table_similarity)  # Convert to integer
        logger.info(f"Overall similarity: {overall_similarity}\n")
        
        if overall_similarity > highest_overall_similarity:
            highest_overall_similarity = overall_similarity
            best_url = found_url
            best_matched_table = most_similar_table
        
        output_data.append({
            "URL": found_url,
            "title": title,
            "table_id": table_id,
            "matched_title": matched_title,
            "title_similarity": title_similarity,
            "table_similarity": table_similarity,
            "overall_similarity": overall_similarity
        })
        
    logger.info(f"URL with highest overall similarity: {best_url}")
    logger.info(f"Best matched table (first 4 rows and columns):\n{extract_first_4x4(best_matched_table)}")
    return output_data, best_url

def save_to_csv(data, filename):
    df = pd.DataFrame(data)
    csv_filename = filename.replace('.json', '.csv')
    df.to_csv(csv_filename, index=False)
    logger.info(f"Saved data to {csv_filename}")

def main():
    for file_name in ['qtsumm_dev.json', 'qtsumm_test.json', 'qtsumm_train.json']:
        data, best_url = load_and_process_file(file_name)
        save_to_csv(data, file_name)
        logger.info(f"URL with highest overall similarity for {file_name}: {best_url}")

if __name__ == "__main__":
    main()
