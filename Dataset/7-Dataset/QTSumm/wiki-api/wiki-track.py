import subprocess
import sys
import os
from urllib.parse import urlparse, parse_qs, unquote
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
            return results[:3]  # Take the top 3 results
    except requests.RequestException as e:
        logger.info(f"Request failed: {e}")
    except json.JSONDecodeError:
        logger.info("Failed to decode JSON from response.")
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
    Retrieve the curid from a Wikipedia URL by accessing the 'Page information' page.

    Parameters:
    url (str): The Wikipedia URL.

    Returns:
    str: The curid of the page.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find the "Page information" link
        page_info_link = soup.find('a', string="Page information")
        if page_info_link:
            page_info_url = f"https://en.wikipedia.org{page_info_link['href']}"
            response = requests.get(page_info_url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract the Page ID
            page_id_row = soup.find('th', string="Page ID")
            if page_id_row:
                page_id = page_id_row.find_next_sibling('td').text.strip()
                return page_id
    except requests.RequestException as e:
        logger.info(f"Request failed: {e}")
    except Exception as e:
        logger.info(f"Error retrieving curid from URL: {e}")
    return ""




# ... [rest of the code remains unchanged]

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

            search_results = search_wikipedia(title)
            top_results = []
            for result in search_results:
                page_id = result['pageid']
                found_url = f"http://en.wikipedia.org/?curid={page_id}"
                matched_title = result['title']
                
                if found_url != "Not found":
                    curid = parse_qs(urlparse(found_url).query)['curid'][0]
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

# ... [rest of the code remains unchanged]




def save_to_csv(data, filename):
    df = pd.DataFrame(data)
    csv_filename = filename.replace('.json', '.csv')
    df.to_csv(csv_filename, index=False)
    logger.info(f"Saved data to {csv_filename}")

def main():
    # Get the current script directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Get the parent directory
    parent_dir = os.path.abspath(os.path.join(current_dir, '..'))

    
   # for file_name in ['test.json']:
    for file_name in ['qtsumm_dev.json', 'qtsumm_test.json', 'qtsumm_train.json']:
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
