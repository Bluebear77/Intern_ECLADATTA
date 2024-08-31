import pandas as pd

# List of CSV files and their corresponding URL column names
csv_files = {
    'LOGICNLG.csv': 'URL',
    'F2WTQ.csv': 'url',
    'FeTaQA.csv': 'converted_url',
    'LOTNLG.csv': 'URL',
    'ToTTo.csv': 'Page ID URL',
    'WTQ.csv': 'URL'
}

# Initialize counter for the total number of unique URLs
total_unique_urls = 0

# Function to remove duplicates in each file and save to a new cleaned file
def remove_duplicates(csv_file, url_column):
    global total_unique_urls
    try:
        # Load the CSV file
        df = pd.read_csv(csv_file)
        
        # Check if the expected URL column exists
        if url_column not in df.columns:
            raise ValueError(f"Expected column '{url_column}' not found in {csv_file}. Available columns: {list(df.columns)}")
        
        # Remove duplicate URLs, keeping the first occurrence
        df_cleaned = df.drop_duplicates(subset=url_column, keep='first')
        
        # Create the cleaned file name
        cleaned_file_name = csv_file.replace('.csv', '-cleaned.csv')
        
        # Save the cleaned DataFrame to a new file
        df_cleaned.to_csv(cleaned_file_name, index=False)
        
        # Update the total unique URLs counter
        total_unique_urls += len(df_cleaned)
        
        # Print the number of rows removed
        num_removed = len(df) - len(df_cleaned)
        print(f"{csv_file}: Number of duplicate URLs removed: {num_removed}")
        print(f"Cleaned data saved to: {cleaned_file_name}")
        
    except Exception as e:
        print(f"Error processing {csv_file}: {e}")

# Remove duplicates for each file and save cleaned files
for file, column in csv_files.items():
    remove_duplicates(file, column)

# Print the total number of unique URLs across all files
print(f"Total number of unique URLs across all files: {total_unique_urls}")
