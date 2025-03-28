import pandas as pd
import matplotlib.pyplot as plt
from matplotlib_venn import venn2

# Input CSV file names
file1 = "personnalites_top_200_pid_op.csv"
file2 = "personnalites_human_annotated_pid_op.csv"

# Load data
df1 = pd.read_csv(file1)
df2 = pd.read_csv(file2)

# Create PID sets
set1 = set(df1["pid"])
set2 = set(df2["pid"])

# Plot Venn diagram
plt.figure(figsize=(6, 6))
venn2([set1, set2], set_labels=("Top 200", "Human Annotated"))
plt.title("Venn Diagram of PIDs")
plt.tight_layout()
plt.savefig("venn_diagram.png")
plt.close()

# Prepare overlap info
only_df1 = df1[df1["pid"].isin(set1 - set2)].copy()
only_df1["Source"] = "Only in Top 200"

only_df2 = df2[df2["pid"].isin(set2 - set1)].copy()
only_df2["Source"] = "Only in Human Annotated"

both = df1[df1["pid"].isin(set1 & set2)].copy()
both["Source"] = "In Both"

# Combine all
comparison_df = pd.concat([only_df1, only_df2, both], ignore_index=True)
comparison_df = comparison_df[["Source", "pid_label", "pid", "count"]]

# Write to Markdown
with open("comparison.md", "w", encoding="utf-8") as f:
    f.write("# PID Comparison Report\n\n")
    f.write("## Venn Diagram\n\n")
    f.write("![Venn Diagram](venn_diagram.png)\n\n")

    f.write("## PID Comparison Table\n\n")
    f.write("| Source | pid_label | pid | count |\n")
    f.write("|--------|-----------|-----|-------|\n")
    for _, row in comparison_df.iterrows():
        f.write(f"| {row['Source']} | {row['pid_label']} | {row['pid']} | {row['count']} |\n")

print("Done! Output written to 'comparison.md'")
