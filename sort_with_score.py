import csv
import requests
from bs4 import BeautifulSoup
import re

def analyze_url(url):
    """Analyze the given URL to check for tables, text diversity, and word count, returning a composite score."""
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        soup = BeautifulSoup(response.text, 'html.parser')
        
        tables = soup.find_all('table')
        if not tables:
            return 0
        
        # Counting unique column names across all tables as a proxy for table diversity
        column_names = set()
        for table in tables:
            for th in table.find_all('th'):
                column_names.add(th.get_text(strip=True))
        
        text = soup.get_text()
        word_count = len(text.split())
        
        # Identifying depth indicators in the text
        depth_keywords = re.findall(r'\banalysis\b|\bcommentary\b|\bsummary\b', text, re.IGNORECASE)
        
        # Simple scoring: (Unique Columns * Weight1) + (Word Count * Weight2) + (Depth Keywords * Weight3)
        # Adjust the weights as needed
        score = (len(column_names) * 2) + (word_count * 0.01) + (len(depth_keywords) * 5)
        return score
    except Exception as e:
        print(f"Error processing {url}: {e}")
    return 0

def process_csv(input_csv, output_csv):
    urls_scores = []
    
    with open(input_csv, mode='r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip header
        for row in reader:
            url = row[1]  # Assuming URLs are in the second column
            score = analyze_url(url)
            if score > 0:
                urls_scores.append((url, score))
    
    # Sort the URLs by score in descending order and keep the top 200
    urls_scores.sort(key=lambda x: x[1], reverse=True)
    top_200 = urls_scores[:200]
    
    # Write the results to an output CSV file
    with open(output_csv, mode='w', encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["URL", "Score"])
        writer.writerows(top_200)

# Example usage
#input_csv_path = 'test.csv'
input_csv_path = 'extracted_all.csv'  # Adjust with the path to your input CSV file
output_csv_path = 'sorted_with_scores.csv'  # The path for the output CSV file
process_csv(input_csv_path, output_csv_path)



'''
0riginal strategy：
select the top 200 URLs that have both tables and text, sorted by the URLs with the most word counts.

Improvements:
Weighted Ranking: Instead of solely sorting by the number of tables or word counts, you could create a weighted ranking system that takes into account both factors. For example, you could assign a higher weight to tables that have diverse columns and data, and also consider the quality and depth of the surrounding text.

Implementation:
Evaluating Table Diversity: Assign points or a weight based on the diversity of the table columns. A simple proxy for this could be the number of different column titles in all tables on the page.

Incorporating Quality and Depth of Text: Besides counting words, analyze the text for indicators of depth or analysis, such as the presence of keywords like "analysis," "commentary," "summary," etc., which could signal more insightful content.
'''
