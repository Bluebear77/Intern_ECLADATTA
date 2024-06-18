import subprocess
import sys
import time
from urllib.parse import urlparse, parse_qs
import random
from io import StringIO
import os

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
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger()

# Create file handler to log to a file
file_handler = logging.FileHandler('log.txt')
file_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

def get_wikipedia_page_id(url):
    try:
        # Extract the title from the URL
        parsed_url = urlparse(url)
        if 'title' in parse_qs(parsed_url.query):
            title = parse_qs(parsed_url.query)['title'][0]
        else:
            title = parsed_url.path.split('/')[-1]
        
        # Make a request to the Wikipedia API to get the page ID
        api_url = f"https://en.wikipedia.org/w/api.php?action=query&titles={title}&format=json"
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()
        
        # Extract the page ID from the API response
        pages = data['query']['pages']
        page_id = next(iter(pages))
        
        if page_id != "-1":  # Ensure page exists
            return page_id
    except requests.RequestException as e:
        logger.info(f"Request failed: {e}")
    return None

def clean_matched_title(matched_title):
    # Remove unwanted parts from matched_title
    if 'wikipedia.org' in matched_title:
        matched_title = matched_title.split('wikipedia.org')[0].strip()
    return matched_title

def search_google(title):
    search_url = f"https://www.google.com/search?q={title.replace(' ', '+')}+site:wikipedia.org"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    top_results = []
    
    while True:
        try:
            response = requests.get(search_url, headers=headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            for link in soup.find_all('a'):
                href = link.get('href')
                if href and 'wikipedia.org' in href:
                    full_url = href.split('&')[0].replace('/url?q=', '')
                    if 'en.wikipedia.org/wiki/' in full_url:
                        page_id = get_wikipedia_page_id(full_url)
                        if page_id:
                            wiki_url = f"http://en.wikipedia.org/?curid={page_id}"
                            top_results.append((wiki_url, clean_matched_title(link.get_text())))
                            if len(top_results) == 3:
                                return top_results
        except requests.RequestException as e:
            if response.status_code == 429:
                logger.info(f"Request failed: {e}. Retrying after a pause...")
                time.sleep(120)  # Wait for a minute before retrying
            else:
                logger.info(f"Request failed: {e}")
                return []
    return top_results


def search_combined(title):
    google_results = search_google(title)
    results = []

    for url, matched_title in google_results:
        title_similarity = fuzz.ratio(title.lower(), matched_title.lower())
        results.append((url, matched_title, title_similarity))

    return results


    return results

def fetch_all_wikipedia_tables(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        tables = soup.find_all('table', {'class': 'wikitable'})
        dataframes = [pd.read_html(StringIO(str(table)))[0] for table in tables]
        return dataframes
    except requests.RequestException as e:
        logger.info(f"Request failed: {e}")
    except Exception as e:
        logger.info(f"Error fetching tables: {e}")
    return []

def extract_first_4x4(df):
    if not df.empty:
        df = df.astype(str)
        return df.iloc[:4, :4].fillna('')
    return pd.DataFrame()

def compare_tables(actual_df, matched_df):
    actual_sub = extract_first_4x4(actual_df)
    matched_sub = extract_first_4x4(matched_df)
    if actual_sub.empty or matched_sub.empty:
        return 0.0
    return fuzz.ratio(actual_sub.to_string(index=False, header=True), matched_sub.to_string(index=False, header=True))

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
    log_file = open('test.txt', 'a')
    
    for item in tqdm(data, desc=f"Processing {filename}"):
        title = item['table']['title']
        table_id = item['table']['table_id']
        
        if 'rows' in item['table']:
            actual_table = pd.DataFrame(item['table']['rows'], columns=item['table']['header'])
        else:
            actual_table = pd.DataFrame()

        logger.info(f"\nProcessing table: {title}\nTable_id: {table_id}")
        logger.info(f"Actual table (first 4 rows and columns):\n{extract_first_4x4(actual_table)}\n")

        google_results = search_combined(title)
        logger.info(f"Found URLs: {[result[0] for result in google_results]}")
        
        best_result = {"overall_similarity": 0}
        
        for found_url, matched_title, title_similarity in google_results:
            logger.info(f"Found URL: {found_url}, Matched Title: {matched_title}")
            logger.info(f"Title similarity: {title_similarity}")

            table_similarity = 0.0
            most_similar_table = pd.DataFrame()
            if found_url != "Not found":
                most_similar_table, table_similarity = find_most_similar_table(found_url, actual_table)
                logger.info(f"Most similar table (first 4 rows and columns):\n{extract_first_4x4(most_similar_table)}")

            logger.info(f"Table similarity: {table_similarity}")

            overall_similarity = int(0.4 * title_similarity + 0.6 * table_similarity)
            logger.info(f"Overall similarity: {overall_similarity}\n")
            
            if overall_similarity > best_result["overall_similarity"]:
                best_result = {
                    "overall_similarity": overall_similarity,
                    "url": found_url,
                    "matched_title": matched_title,
                    "title_similarity": title_similarity,
                    "table_similarity": table_similarity,
                    "most_similar_table": most_similar_table
                }
        
        if best_result["overall_similarity"] > highest_overall_similarity:
            highest_overall_similarity = best_result["overall_similarity"]
            best_url = best_result["url"]
            best_matched_table = best_result["most_similar_table"]
        
        output_data.append({
            "URL": best_result["url"],
            "title": title,
            "table_id": table_id,
            "matched_title": best_result["matched_title"],
            "title_similarity": best_result["title_similarity"],
            "table_similarity": best_result["table_similarity"],
            "overall_similarity": best_result["overall_similarity"]
        })
        
        # Log the matched URL and full table to the test.txt file
        log_file.write(f"Matched URL: {best_result['url']}\n")
        log_file.write(f"Table Title: {title}\n")
        log_file.write(f"Matched Table:\n{best_result['most_similar_table'].to_string(index=False)}\n\n")
        
    logger.info(f"URL with highest overall similarity: {best_url}")
    logger.info(f"Best matched table (first 4 rows and columns):\n{extract_first_4x4(best_matched_table)}")
    
    log_file.close()
    return output_data, best_url


def save_to_csv(data, filename):
    df = pd.DataFrame(data)
    csv_filename = filename.replace('.json', '.csv')
    df.to_csv(csv_filename, index=False)
    logger.info(f"Saved data to {csv_filename}")


def main():
    dev_directory = './dev/'
    json_files = [f for f in os.listdir(dev_directory) if f.endswith('.json')]
    
    # Check for existing .csv files and filter json_files
    json_files_to_process = [f for f in json_files if not os.path.exists(os.path.join(dev_directory, f.replace('.json', '.csv')))]
    
    for file_name in json_files_to_process:
        full_path = os.path.join(dev_directory, file_name)
        data, best_url = load_and_process_file(full_path)
        save_to_csv(data, full_path)
        logger.info(f"URL with highest overall similarity for {file_name}: {best_url}")


if __name__ == "__main__":
    main()

'''




def main():
    # Get the current script directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Get the parent directory
    parent_dir = os.path.abspath(os.path.join(current_dir, '..'))

    
   # for file_name in ['test.json']:
    for file_name in ['test.json']:
        # Construct the full file path to the parent directory
        file_path = os.path.join(parent_dir, file_name)

        # Process the file
        data, best_url = load_and_process_file(file_path)

        # Save the processed data to a CSV
        save_to_csv(data, file_name)

        # Log the URL with the highest overall similarity
        logger.info(f"URL with highest overall similarity for {file_name}: {best_url}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()

'''