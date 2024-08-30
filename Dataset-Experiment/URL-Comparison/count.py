import pandas as pd

# List of CSV files and their corresponding URL column names
cleaned_csv_files = {
    'LOGICNLG-cleaned.csv': 'URL',
    'F2WTQ-cleaned.csv': 'url',
    'FeTaQA-cleaned.csv': 'converted_url',
    'LOTNLG-cleaned.csv': 'URL',
    'ToTTo-cleaned.csv': 'Page ID URL',
    'WTQ-cleaned.csv': 'URL',
    'telco100.csv': 'URL1',
    'business100.csv': 'URL1',
    'female100_english.csv': 'URL'
}

original_csv_files = {
    'LOGICNLG.csv': 'URL',
    'F2WTQ.csv': 'url',
    'FeTaQA.csv': 'converted_url',
    'LOTNLG.csv': 'URL',
    'ToTTo.csv': 'Page ID URL',
    'WTQ.csv': 'URL',
    'telco100.csv': 'URL1',
    'business100.csv': 'URL1',
    'female100_english.csv': 'URL'
}

# Initialize counters for the total number of unique and total URLs
total_unique_urls = 0
total_urls = 0

# Process cleaned files (unique URLs)
for file, url_column in cleaned_csv_files.items():
    try:
        # Load the CSV file
        df = pd.read_csv(file)
        
        # Check if the expected URL column exists
        if url_column not in df.columns:
            raise ValueError(f"Expected column '{url_column}' not found in {file}. Available columns: {list(df.columns)}")
        
        # Count the number of unique URLs in this file
        unique_urls_count = df[url_column].nunique()
        
        # Print the unique URL count for this file
        print(f"{file}: Number of unique URLs: {unique_urls_count}")
        
        # Add the unique count to the total unique URLs
        total_unique_urls += unique_urls_count
        
    except Exception as e:
        print(f"Error processing {file}: {e}")

# Process original files (total URLs)
for file, url_column in original_csv_files.items():
    try:
        # Load the CSV file
        df = pd.read_csv(file)
        
        # Check if the expected URL column exists
        if url_column not in df.columns:
            raise ValueError(f"Expected column '{url_column}' not found in {file}. Available columns: {list(df.columns)}")
        
        # Count the total number of URLs in this file
        total_urls_count = len(df[url_column])
        
        # Print the total URL count for this file
        print(f"{file}: Number of total URLs: {total_urls_count}")
        
        # Add the total count to the total URLs
        total_urls += total_urls_count
        
    except Exception as e:
        print(f"Error processing {file}: {e}")

# Print the total number of unique URLs and total URLs across all files
print(f"Total number of unique URLs across cleaned files: {total_unique_urls}")
print(f"Total number of URLs across original files: {total_urls}")
