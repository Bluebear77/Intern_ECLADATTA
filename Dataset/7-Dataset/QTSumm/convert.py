import requests

def get_wikipedia_page_id(url):
    try:
        # Extract the title from the URL
        title = url.split('title=')[-1]
        
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
        print(f"Request failed: {e}")
    return None

# Testing the function with the provided URL
url = "https://en.wikipedia.org/w/index.php?title=List_of_tallest_buildings_in_Fort_Wayne"
page_id = get_wikipedia_page_id(url)

# Printing the formatted URL
if page_id:
    formatted_url = f"http://en.wikipedia.org/?curid={page_id}"
else:
    formatted_url = "Page ID not found"

print(formatted_url)
