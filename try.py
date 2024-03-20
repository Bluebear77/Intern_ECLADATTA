import csv
import requests
from bs4 import BeautifulSoup

def analyze_url(url):
    """Analyze the given URL to check for tables and text, returning the word count."""
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        soup = BeautifulSoup(response.text, 'html.parser')
        tables = soup.find_all('table')
        text_words = soup.get_text().split()
        if tables and text_words:
            return len(text_words)
    except Exception as e:
        print(f"Error processing {url}: {e}")
    return 0

def process_csv(input_csv, output_csv):
    urls_word_counts = []
    
    with open(input_csv, mode='r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip header
        for row in reader:
            url = row[1]  # Assuming URLs are in the second column
            word_count = analyze_url(url)
            if word_count:
                urls_word_counts.append((url, word_count))
    
    # Sort the URLs by word count in descending order and keep the top 200
    urls_word_counts.sort(key=lambda x: x[1], reverse=True)
    top_200 = urls_word_counts[:200]
    
    # Write the results to an output CSV file
    with open(output_csv, mode='w', encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["URL", "Word Count"])
        writer.writerows(top_200)

# Example usage
#input_csv_path = 'test.csv'
input_csv_path = 'extracted_all.csv'  # Adjust with the path to your input CSV file
output_csv_path = 'sort.csv'  # The path for the output CSV file
process_csv(input_csv_path, output_csv_path)

