import subprocess
import sys
import os
from urllib.parse import urlparse, parse_qs, unquote
from io import StringIO
import glob

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
file_handler = logging.FileHandler('log2.txt')
file_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

def is_disambiguation_page(curid):
    """
    Check if a Wikipedia page is a disambiguation page.

    Parameters:
    curid (str): The curid of the Wikipedia page.

    Returns:
    bool: True if it is a disambiguation page, False otherwise.
    """
    url = f"https://en.wikipedia.org/w/api.php"
    params = {
        'action': 'query',
        'pageids': curid,
        'prop': 'pageprops',
        'format': 'json'
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    
    try:
        pageprops = data['query']['pages'][curid]['pageprops']
        if 'disambiguation' in pageprops:
            return True
    except KeyError:
        # If the page does not exist or has no pageprops
        return False
    
    return False

def search_google(title):
    search_url = f"https://www.google.com/search?q={title.replace(' ', '+')}+site:wikipedia.org"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(search_url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        results = []
        for link in soup.find_all('a'):
            href = link.get('href')
            if href and 'wikipedia.org' in href:
                full_url = href.split('&')[0].replace('/url?q=', '')
                if 'en.wikipedia.org/wiki/' in full_url:
                    results.append(full_url)
                    if len(results) == 3:
                        break
        return results
    except requests.RequestException as e:
        if response.status_code == 429:
            logger.info(f"Request failed: {e}. Retrying after a pause...")
            time.sleep(120)  # Wait for a minute before retrying
        else:
            logger.info(f"Request failed: {e}")
            return []
    return []

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

def explore_disambiguation_page(url, input_df):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        links = soup.find_all('a', href=True)
        highest_score = 0
        most_similar_table = pd.DataFrame()
        best_url = ""

        for link in links:
            href = link['href']
            if href.startswith('/wiki/') and not href.startswith('/wiki/Special:'):
                full_url = f"https://en.wikipedia.org{href}"
                table, score = find_most_similar_table(full_url, input_df)
                if score > highest_score:
                    highest_score = score
                    most_similar_table = table
                    best_url = full_url

        return most_similar_table, highest_score, best_url

    except requests.RequestException as e:
        logger.info(f"Request failed: {e}")
    except Exception as e:
        logger.info(f"Error exploring disambiguation page: {e}")
    return pd.DataFrame(), 0.0, ""
def get_curid_from_url(url):
    """
    Retrieve the curid from a Wikipedia URL using the Wikipedia API.

    Parameters:
    url (str): The Wikipedia URL.

    Returns:
    str: The curid URL of the page in the format `https://en.wikipedia.org/?curid=xxxx`.
    """
    try:
        # Extract the page title from the URL
        title = url.split('/')[-1]
        
        # Use the Wikipedia API to get page info
        api_url = f"https://en.wikipedia.org/w/api.php?action=query&titles={title}&format=json"
        response = requests.get(api_url)
        response.raise_for_status()
        
        data = response.json()
        page = next(iter(data['query']['pages'].values()))
        curid = str(page['pageid'])
        return f"https://en.wikipedia.org/?curid={curid}"
    
    except requests.RequestException as e:
        print(f"Request failed: {e}")
    except Exception as e:
        print(f"Error retrieving curid from URL: {e}")
    
    return ""


def load_and_process_file(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
    
    output_data = []
    highest_overall_similarity = 0
    best_url = "Not found"
    best_matched_table = pd.DataFrame()
    
    with open('tables-log.txt', 'w') as f:  # Open file once for writing
        for item in tqdm(data, desc=f"Processing {filename}"):
            title = item['table']['title']
            table_id = item['table']['table_id']
            
            if 'rows' in item['table']:
                actual_table = pd.DataFrame(item['table']['rows'], columns=item['table']['header'])
            else:
                actual_table = pd.DataFrame()

            logger.info(f"\nProcessing table: {title} with table_id: {table_id}")
            logger.info(f"Actual table (first 4 rows and columns):\n{extract_first_4x4(actual_table)}\n")

            search_results = search_google(title)
            top_results = []
            for found_url in search_results:
                matched_title = found_url.split('/')[-1].replace('_', ' ')
                
                if found_url != "Not found":
                    curid = get_curid_from_url(found_url)
                    if is_disambiguation_page(curid):
                        logger.info(f"The page with curid={curid} is a disambiguation page.")
                        most_similar_table, table_similarity, best_url = explore_disambiguation_page(found_url, actual_table)
                    else:
                        logger.info(f"The page with curid={curid} is not a disambiguation page.")
                        most_similar_table, table_similarity = find_most_similar_table(found_url, actual_table)
                        best_url = found_url
                else:
                    table_similarity = 0.0
                
                title_similarity = fuzz.ratio(title.lower(), matched_title.lower()) if found_url != "Not found" else 0.0
                logger.info(f"Title similarity: {title_similarity}")
                
                logger.info(f"Most similar table (first 4 rows and columns):\n{extract_first_4x4(most_similar_table)}\n")
                logger.info(f"Table similarity: {table_similarity}\n")
                
                overall_similarity = int(0.4 * title_similarity + 0.6 * table_similarity)  # Convert to integer
                
                logger.info(f"Overall similarity: {overall_similarity}\n")
                
                top_results.append((best_url, matched_title, title_similarity, table_similarity, overall_similarity, most_similar_table))

            top_results.sort(key=lambda x: x[4], reverse=True)  # Sort by overall_similarity
            
            if top_results:
                best_url, best_matched_title, _, _, _, best_matched_table = top_results[0]
            
            output_data.append({
                "URL": best_url,
                "title": title,
                "table_id": table_id,
                "matched_title": best_matched_title,
                "title_similarity": top_results[0][2] if top_results else 0.0,
                "table_similarity": top_results[0][3] if top_results else 0.0,
                "overall_similarity": top_results[0][4] if top_results else 0.0
            })
            
            if best_url != "Not found":
                final_curid = get_curid_from_url(best_url)
                if final_curid:
                    best_url = f"http://en.wikipedia.org/?curid={final_curid}"
            
            # Write to test.txt: URL and full matched table for each URL
            f.write(best_url + "\n")
            f.write(best_matched_table.to_string(index=False) + "\n\n")
            
            logger.info(f"URL with highest overall similarity: {best_url}")
            logger.info(f"Best matched table (first 4 rows and columns):\n{extract_first_4x4(best_matched_table)}")
            logger.info(f"Full matched table:\n{best_matched_table.to_string(index=False)}")

    return output_data, best_url

def save_to_csv(data, filename):
    df = pd.DataFrame(data)
    csv_filename = filename.replace('.json', '.csv')
    df.to_csv(csv_filename, index=False)
    logger.info(f"Saved data to {csv_filename}")


# for file_name in ['qtsumm_dev.json', 'qtsumm_test.json', 'qtsumm_train.json']:


def main():
    # Get the current script directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Construct the full path to the dev directory
    dev_dir = os.path.join(current_dir, 'dev')

    # Find all .json files in the dev directory
    json_files = glob.glob(os.path.join(dev_dir, 'qtsumm_dev_chunk_*.json'))

    for json_file in json_files:
        # Corresponding .csv file name
        csv_file = json_file.replace('.json', '.csv')

        # Check if the corresponding .csv file exists
        if not os.path.exists(csv_file):
            # Process the file
            data, best_url = load_and_process_file(json_file)

            # Save the processed data to a CSV
            save_to_csv(data, json_file)

            # Log the URL with the highest overall similarity
            logger.info(f"URL with highest overall similarity for {json_file}: {best_url}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()

