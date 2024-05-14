import pandas as pd

# Read the CSV file
df = pd.read_csv('boolean.csv')

# Filter the rows where primitiveTyping is True (T)
true_files = df[df['primitiveTyping'] == 'T']

# Select the 'filename' column and save it to 'true.csv'
true_files[['filename']].to_csv('true.csv', index=False)

print("Filtered filenames have been saved to 'true.csv'.")
