import json
import pandas as pd
from collections import defaultdict

# Load the JSON file
json_path = "Female_Celebrity_FR.json"
with open(json_path, "r", encoding="utf-8") as file:
    data = json.load(file)

# Dictionary to store entityValue counts and titles
entity_counts = defaultdict(lambda: {"count": 0, "examples": set(), "label": ""})

# Iterate through documents
for document in data["documents"]:
    title = document["title"]
    
    for annotation in document.get("annotations", []):
        predicate = annotation.get("predicate", {})
        entity_label = predicate.get("entityLabel", "")
        entity_value = predicate.get("entityValue", "")

        if entity_value:
            entity_counts[entity_value]["count"] += 1
            entity_counts[entity_value]["examples"].add(title)
            entity_counts[entity_value]["label"] = entity_label

# Convert to DataFrame
df = pd.DataFrame([
    {"pid_label": details["label"], 
     "pid": entity, 
     "count": details["count"], 
     "examples": ", ".join(details["examples"])}
    for entity, details in sorted(entity_counts.items(), key=lambda x: x[1]["count"], reverse=True)
])

# Save to CSV
csv_output_path = "personnalites_human_annotated_pid_op.csv"
df.to_csv(csv_output_path, index=False, encoding="utf-8")

print(f"CSV file saved to {csv_output_path}")
