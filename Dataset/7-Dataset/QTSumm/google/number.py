import os

# Set the directory you want to search
directory = './train'

# Initialize counters
csv_count = 0
json_count = 0

# Walk through directory
for root, dirs, files in os.walk(directory):
    for file in files:
        if file.endswith('.csv'):
            csv_count += 1
        elif file.endswith('.json'):
            json_count += 1

# Output the counts
print(f'Total number of .csv files: {csv_count}')
print(f'Total number of .json files: {json_count}')
