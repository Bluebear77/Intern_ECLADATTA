import os
import json
from collections import defaultdict

# Paths to the JSON files
json_files = [
    "../qtsumm_test.json",
    "../qtsumm_dev.json",
    "../qtsumm_train.json"
]

# Dictionary to store tables by title and the files they appear in
tables_by_title = defaultdict(lambda: {"sources": [], "tables": []})

# Iterate through each file and extract tables by title
for file_path in json_files:
    with open(file_path, 'r') as file:
        data = json.load(file)
        for item in data:
            title = item["table"]["title"]
            table_id = item["table"]["table_id"]
            source = os.path.basename(file_path)
            tables_by_title[title]["sources"].append(source)
            tables_by_title[title]["tables"].append({
                "table_id": table_id,
                "source": source,
                "table": item["table"]
            })

# Filter to include only tables that appear in two or more different files
filtered_tables = {
    title: info for title, info in tables_by_title.items()
    if len(set(info["sources"])) > 1
}

# Create Markdown and JSON output
md_lines = ["| Title | Table ID | Source |", "|-------|----------|--------|"]
json_output = []

for title, info in filtered_tables.items():
    for table_info in info["tables"]:
        table_id = table_info["table_id"]
        source = table_info["source"]
        md_lines.append(f"| {title} | {table_id} | {source} |")
        json_output.append(table_info["table"])

# Write Markdown file
with open("tables_summary.md", "w") as md_file:
    md_file.write("\n".join(md_lines))

# Write JSON file
with open("tables_summary.json", "w") as json_file:
    json.dump(json_output, json_file, indent=4)

print("Markdown and JSON files have been generated.")
