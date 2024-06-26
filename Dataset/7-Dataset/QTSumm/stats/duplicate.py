import json
import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm

# File paths pointing to the parent directory
files = {
    'qtsumm_test.json': '../qtsumm_test.json',
    'qtsumm_dev.json': '../qtsumm_dev.json',
    'qtsumm_train.json': '../qtsumm_train.json'
}

# To store the table data
table_data = []

# To track tables across files
table_titles = {}

# Read each file and process data
for filename, filepath in tqdm(files.items(), desc="Processing files"):
    with open(filepath, 'r') as file:
        data = json.load(file)
        for entry in tqdm(data, desc=f"Processing {filename}", leave=False):
            title = entry['table']['title']
            table_id = entry['table']['table_id']
            table_data.append({'title': title, 'table_id': table_id, 'source': filename})
            
            if title in table_titles:
                found = False
                for item in table_titles[title]:
                    if item['table_id'] == table_id:
                        item['source'].append(filename)
                        found = True
                        break
                if not found:
                    table_titles[title].append({'table_id': table_id, 'source': [filename]})
            else:
                table_titles[title] = [{'table_id': table_id, 'source': [filename]}]

# Convert to DataFrame for easier manipulation
df = pd.DataFrame(table_data)

# Create markdown file with the tables' details
markdown_table = df.pivot_table(index=['title', 'table_id'], values='source', aggfunc=lambda x: ', '.join(set(x))).reset_index()
markdown_table.to_markdown('table_details.md', index=False)

# Create JSON file with table titles data
with open('table_titles.json', 'w') as jsonfile:
    json.dump(table_titles, jsonfile, indent=4)

# Plotting the frequency of table titles
title_counts = df['title'].value_counts()
title_counts.plot(kind='bar')
plt.title('Frequency of Table Titles Across Files')
plt.xlabel('Table Titles')
plt.ylabel('Frequency')
plt.savefig('title_frequency.png')
plt.show()
