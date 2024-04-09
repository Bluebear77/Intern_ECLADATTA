import requests

def get_wikipedia_page_id(url):
    # Extract the title from the given URL
    title = url.split('/wiki/')[-1]
    
    # Prepare the API request parameters
    params = {
        'action': 'query',
        'prop': 'pageprops',
        'titles': title,
        'format': 'json'
    }
    api_url = "https://en.wikipedia.org/w/api.php"
    
    try:
        # Make the request to Wikipedia's API
        response = requests.get(api_url, params=params)
        response.raise_for_status()  # Raise an error for bad responses
        
        # Parse the JSON response
        data = response.json()
        
        # Extract the page ID from the JSON response
        pages = data.get('query', {}).get('pages', {})
        page_id = next(iter(pages.keys()))  # Get the first key in the 'pages' dictionary
        
        if page_id == "-1":
            print("Page not found")
        else:
            # Construct and print the correct URL
            correct_url = f"http://en.wikipedia.org/?curid={page_id}"
            print(f"Found page ID: {page_id}")
            print(f"Correct URL: {correct_url}")
            
    except requests.RequestException as e:
        print(f"Error: {e}")

# Test the function with the given URL
test_url = "http://en.wikipedia.org/wiki/Dodge_Charger_(LX/LD)"
get_wikipedia_page_id(test_url)
