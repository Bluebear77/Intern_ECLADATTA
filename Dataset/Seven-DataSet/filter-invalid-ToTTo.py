import csv

input_file = 'ToTTO-Page-ID-URLs.csv'
output_file = 'Invalid-ToTTo-Page-ID-URLs.csv'

with open(input_file, newline='', encoding='utf-8') as infile, open(output_file, 'w', newline='', encoding='utf-8') as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)
    
    # Write header to output file
    header = next(reader)
    writer.writerow(header)
    
    # Filter and write rows where Page ID URL ends with "curid=-1"
    for row in reader:
        if row[1].endswith('curid=-1'):
            writer.writerow(row)
