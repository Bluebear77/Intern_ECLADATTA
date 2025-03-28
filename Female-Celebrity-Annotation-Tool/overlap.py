import pandas as pd
import matplotlib.pyplot as plt
from matplotlib_venn import venn2
import json

# Load CSVs
df1 = pd.read_csv("personnalites_top_200_pid_op.csv")
df2 = pd.read_csv("personnalites_human_annotated_pid_op.csv")

# Create PID sets
set1 = set(df1["pid"])
set2 = set(df2["pid"])

# Venn Diagram
plt.figure(figsize=(6, 6))
venn2([set1, set2], set_labels=("Top 200", "Human Annotated"))
plt.title("Venn Diagram of PIDs")
plt.tight_layout()
plt.savefig("venn_diagram.png")
plt.close()

# Overlap Table
only_df1 = df1[df1["pid"].isin(set1 - set2)].copy()
only_df1["Source"] = "Only in Top 200"

only_df2 = df2[df2["pid"].isin(set2 - set1)].copy()
only_df2["Source"] = "Only in Human Annotated"

both = df1[df1["pid"].isin(set1 & set2)].copy()
both["Source"] = "In Both"

comparison_df = pd.concat([only_df1, only_df2, both], ignore_index=True)
comparison_df = comparison_df[["Source", "pid_label", "pid", "count"]]

# Line Chart for df2
df2_sorted = df2.sort_values(by="count")
plt.figure(figsize=(12, 5))
plt.plot(df2_sorted["pid_label"], df2_sorted["count"], marker="o")
plt.xticks(rotation=90, fontsize=8)
plt.ylabel("Count")
plt.title("Triplet Count by PID Label (Human Annotated)")
plt.tight_layout()
plt.savefig("line_chart.png")
plt.close()

# Empty Triplet Report
with open("Female_Celebrity_FR.json", "r", encoding="utf-8") as f:
    data = json.load(f)

empty_rows = []
empty_counts = {"subject": 0, "predicate": 0, "object": 0}

for doc in data["documents"]:
    title = doc.get("title", "")
    for ann in doc.get("annotations", []):
        sub_val = ann["subject"].get("entityValue", "")
        pre_val = ann["predicate"].get("entityValue", "")
        obj_val = ann["object"].get("entityValue", "")
        row = {
            "title": title,
            "subject": sub_val if sub_val else "empty",
            "predicate": pre_val if pre_val else "empty",
            "object": obj_val if obj_val else "empty"
        }
        if not sub_val or not pre_val or not obj_val:
            if not sub_val:
                empty_counts["subject"] += 1
            if not pre_val:
                empty_counts["predicate"] += 1
            if not obj_val:
                empty_counts["object"] += 1
            empty_rows.append(row)

# Write Markdown Report
with open("comparison.md", "w", encoding="utf-8") as f:
    f.write("# PID Comparison Report\n\n")

    f.write("## Venn Diagram\n\n")
    f.write("![Venn Diagram](venn_diagram.png)\n\n")

    f.write("## PID Comparison Table\n\n")
    f.write("| Source | pid_label | pid | count |\n")
    f.write("|--------|-----------|-----|-------|\n")
    for _, row in comparison_df.iterrows():
        f.write(f"| {row['Source']} | {row['pid_label']} | {row['pid']} | {row['count']} |\n")

    f.write("\n## Line Chart of Human Annotated Counts\n\n")
    f.write("![Line Chart](line_chart.png)\n\n")

    f.write("## Empty Triplet Annotations\n\n")
    f.write("| Title | Subject | Predicate | Object |\n")
    f.write("|-------|---------|-----------|--------|\n")
    for row in empty_rows:
        f.write(f"| {row['title']} | {row['subject']} | {row['predicate']} | {row['object']} |\n")
    f.write(f"| **Total Empty** | {empty_counts['subject']} | {empty_counts['predicate']} | {empty_counts['object']} |\n")

print("✅ Markdown report generated: comparison.md")
