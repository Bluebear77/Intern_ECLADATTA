import requests
import json
from fuzzywuzzy import fuzz
from tqdm import tqdm
import csv

def search_wikipedia(query):
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "list": "search",
        "srsearch": query,
        "format": "json"
    }
    response = requests.get(url, params=params)
    return response.json()

def fetch_wikipedia_page(pageid):
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "parse",
        "pageid": pageid,
        "format": "json"
    }
    response = requests.get(url, params=params)
    return response.json()

def calculate_similarity(original_content, candidate_content):
    return fuzz.ratio(original_content, candidate_content)

def get_table_content(table):
    header = " | ".join(table["header"])
    rows = [" | ".join(map(str, row)) for row in table["rows"]]
    return header + "\n" + "\n".join(rows)

def get_unique_content(table):
    unique_content = []
    for row in table["rows"]:
        unique_content.append(" | ".join(map(str, row)))
        if len(unique_content) >= 3:  # Limit to the first 3 rows for uniqueness
            break
    return ". ".join(unique_content)

def main():
    input_file = "./newdev.json"
    output_file = "./output_urls.csv"

    with open(input_file, 'r') as file:
        data = json.load(file)

    results = []

    for entry in tqdm(data):
        table_title = entry["table"]["title"]
        unique_content = get_unique_content(entry["table"])
        search_query = f"{table_title} {unique_content}"
        table_content = get_table_content(entry["table"])
        
        search_results = search_wikipedia(search_query)
        
        if 'query' not in search_results or 'search' not in search_results['query']:
            continue
        
        candidates = []
        for result in search_results["query"]["search"]:
            pageid = result["pageid"]
            page = fetch_wikipedia_page(pageid)
            if "parse" in page:
                text = page["parse"]["text"]["*"]
                similarity = calculate_similarity(table_content, text)
                candidates.append((pageid, result["title"], similarity))
        
        candidates = sorted(candidates, key=lambda x: x[2], reverse=True)[:5]

        result_entry = [table_title]
        for candidate in candidates:
            url = f"https://en.wikipedia.org/?curid={candidate[0]}"
            result_entry.extend([url, candidate[1], candidate[2]])
        
        results.append(result_entry)

    with open(output_file, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        header = ["Origin Table Title", "URL1", "Title1", "Score1", "URL2", "Title2", "Score2", "URL3", "Title3", "Score3", "URL4", "Title4", "Score4", "URL5", "Title5", "Score5"]
        csvwriter.writerow(header)
        csvwriter.writerows(results)

    print(f"Results saved to {output_file}")

if __name__ == "__main__":
    main()
