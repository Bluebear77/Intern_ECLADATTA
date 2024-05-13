
import re
import pandas as pd

def extract_urls_using_regex(file_path):
    # Read the whole file content into a single string
    with open(file_path, 'r') as file:
        content = file.read()
    
    # Define the regex pattern to find URLs
    # This pattern looks for "url": ["URL1", "URL2"]
    pattern = r'"url": \["(https?://[^"]+)", "(https?://[^"]+)"\]'
    
    # Use regex to find all matches
    matches = re.findall(pattern, content)
    
    # Convert list of tuples to a DataFrame
    if matches:
        df = pd.DataFrame(matches, columns=['URL1', 'URL2'])
    else:
        df = pd.DataFrame(columns=['URL1', 'URL2'])
        
    return df

def save_urls_to_csv(urls_df, output_file_name):
    # Save the DataFrame to CSV
    urls_df.to_csv(output_file_name, index=False)

# File paths
business_file_path = 'wikipedia_en_business100_en_doc.json'
telco_file_path = 'wikipedia_en_telco100_en_doc.json'

# Extract URLs and save to CSV
business_urls_df = extract_urls_using_regex(business_file_path)
save_urls_to_csv(business_urls_df, 'business100.csv')

telco_urls_df = extract_urls_using_regex(telco_file_path)
save_urls_to_csv(telco_urls_df, 'telco100.csv')
