import pandas as pd

# Load the CSV file
df = pd.read_csv('b.csv')

# Function to extract the numeric part from the filename
def extract_number(filename):
    return int(filename.split('_')[1].split('.')[0])

# Apply the function to create a new column for sorting
df['sort_key'] = df['filename'].apply(extract_number)

# Sort the DataFrame based on the newly created sort_key
df_sorted = df.sort_values(by='sort_key')

# Drop the sort_key column as it's no longer needed
df_sorted = df_sorted.drop(columns=['sort_key'])

# Save the sorted DataFrame to a new CSV file
df_sorted.to_csv('sorted_b.csv', index=False)

print("Data sorted and saved to sorted_b.csv.")
