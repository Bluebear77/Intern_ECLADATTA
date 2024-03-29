import csv

# Load invalid URLs
invalid_urls = set()
with open('ToTTo-Invalid-Page-ID-URLs.csv', mode='r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        invalid_urls.add(row['table_webpage_url'])

# Filter ToTTO-Page-ID-URLs, excluding any that are in the invalid set
valid_rows = []
with open('ToTTO-Page-ID-URLs.csv', mode='r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    fields = reader.fieldnames
    for row in reader:
        if row['table_webpage_url'] not in invalid_urls:
            valid_rows.append(row)

# Write the filtered rows to a new file
with open('ToTTO-Page-ID-URLs_filtered.csv', mode='w', encoding='utf-8', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=fields)
    writer.writeheader()
    writer.writerows(valid_rows)

print("Filtered file written successfully.")

