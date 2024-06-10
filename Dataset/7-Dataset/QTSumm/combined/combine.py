import pandas as pd
import os

# Define the file names
files = ["qtsumm_dev.csv", "qtsumm_test.csv", "qtsumm_train.csv"]

# Function to calculate the combined score
def calculate_combined_score(row):
    return int(0.7 * row['title_similarity'] + 0.3 * row['table_similarity'])

# Function to process a single pair of files
def process_files(wiki_file, google_file, output_file):
    # Read the CSV files
    wiki_df = pd.read_csv(wiki_file)
    google_df = pd.read_csv(google_file)

    # Ensure the dataframes have the same length
    if len(wiki_df) != len(google_df):
        raise ValueError(f"Mismatch in number of rows: {wiki_file} and {google_file}")

    # Calculate combined scores
    wiki_df['combined_score'] = wiki_df.apply(calculate_combined_score, axis=1)
    google_df['combined_score'] = google_df.apply(calculate_combined_score, axis=1)

    # Select the row with the highest combined score
    optimal_df = pd.DataFrame()
    optimal_df = wiki_df.where(wiki_df['combined_score'] >= google_df['combined_score'], google_df)

    # Drop the combined score column before saving
    optimal_df.drop(columns=['combined_score'], inplace=True)

    # Save the optimal dataframe to a new CSV file
    optimal_df.to_csv(output_file, index=False)

# Process each pair of files
for file in files:
    wiki_file_path = os.path.join("..", "wiki-api", file)
    google_file_path = os.path.join("..", "google", file)
    output_file_path = file  # Output file in the current directory

    process_files(wiki_file_path, google_file_path, output_file_path)

print("Processing complete. Optimal files are saved in the current directory.")
