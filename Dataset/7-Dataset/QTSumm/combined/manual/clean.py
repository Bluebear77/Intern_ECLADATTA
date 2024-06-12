import pandas as pd

# Load the CSV file into a DataFrame
file_path = 'manual-verified.csv'
df = pd.read_csv(file_path)

# Remove duplicate rows
df_cleaned = df.drop_duplicates()

# Save the cleaned DataFrame back to a CSV file
output_file_path = 'manual-verified-cleaned.csv'
df_cleaned.to_csv(output_file_path, index=False)

print(f"Duplicate rows have been removed. Cleaned data saved to {output_file_path}")
