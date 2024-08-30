
import pandas as pd
import requests

# Read the CSV file
df = pd.read_csv('female100.csv')

# Function to get the English URL from the French URL
def get_english_url(french_url):
    try:
        # Extract the curid value from the French URL
        curid = french_url.split('curid=')[1]
        
        # Use the Wikipedia API to get the English page ID
        api_url = f'https://fr.wikipedia.org/w/api.php?action=query&prop=langlinks&pageids={curid}&lllang=en&format=json'
        response = requests.get(api_url)
        response.raise_for_status()
        
        data = response.json()
        
        # Get the English page title
        page_data = data['query']['pages'][curid]
        if 'langlinks' not in page_data:
            print(f"No English version found for URL {french_url}")
            return french_url
        
        english_title = page_data['langlinks'][0]['*']
        
        # Use the English page title to get the English page ID
        api_url_en = f'https://en.wikipedia.org/w/api.php?action=query&titles={english_title}&format=json'
        response_en = requests.get(api_url_en)
        response_en.raise_for_status()
        
        data_en = response_en.json()
        page_id_en = list(data_en['query']['pages'].keys())[0]
        
        # Create the English URL using the page ID
        english_url = f'https://en.wikipedia.org/?curid={page_id_en}'
        return english_url
    except Exception as e:
        print(f"Error converting URL {french_url}: {e}")
        return french_url

# Apply the conversion function to the URL column
df['URL'] = df['URL'].apply(get_english_url)

# Save the updated dataframe to a new CSV file
df.to_csv('female100_english.csv', index=False)

print("Conversion complete. The updated CSV file is saved as 'female100_english.csv'.")
