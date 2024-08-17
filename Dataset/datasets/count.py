import pandas as pd

# List of CSV files and their corresponding URL column names
csv_files = {
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

# Initialize counter for the total number of unique URLs
total_unique_urls = 0

# Loop through each file and its corresponding URL column
for file, url_column in csv_files.items():
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
        
        # Add the unique count to the total
        total_unique_urls += unique_urls_count
        
    except Exception as e:
        print(f"Error processing {file}: {e}")

# Print the total number of unique URLs across all files
print(f"Total number of unique URLs across all files: {total_unique_urls}")
