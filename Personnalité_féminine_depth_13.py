import requests
from bs4 import BeautifulSoup
import time
from urllib.parse import urljoin

def fetch_categories(category_url, depth, current_depth=1):
    if current_depth > depth:
        return

    try:
        response = requests.get(category_url)
        response.raise_for_status()  # Raises an HTTPError if the status is 4xx, 5xx
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    categories = soup.find_all('a', href=True, title=True)  # Look for 'a' tags with both 'href' and 'title'

    for category in categories:
        if 'Category:' in category['title']:  # Filter for category links
            category_name = category.text
            category_href = category.get('href')
            full_url = urljoin('https://fr.wikipedia.org', category_href)
            print('  ' * (current_depth - 1) + category_name)
            fetch_categories(full_url, depth, current_depth + 1)
            time.sleep(1)  # Be nice to Wikipedia's servers
            
'''
## Save to an output file:

# Specify the output file name
output_file_name = 'wikipedia_categories_depth_13.txt'

start_url = 'https://fr.wikipedia.org/wiki/Catégorie:Personnalité_féminine'

# Open the output file and start fetching categories, writing the results to the file
with open(output_file_name, 'w', encoding='utf-8') as file:
    fetch_categories(start_url, 13, file=file)

print(f"Categories have been written to {output_file_name}")
'''

start_url = 'https://fr.wikipedia.org/wiki/Catégorie:Personnalité_féminine'
fetch_categories(start_url, 13)






