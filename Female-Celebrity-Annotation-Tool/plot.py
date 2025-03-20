import pandas as pd
import matplotlib.pyplot as plt

# Load the generated CSV file
df = pd.read_csv("personnalites_human_annotated_pid_op.csv")

# Select top 10 entities for better visualization
top_df = df.nlargest(10, 'count')

# Bar Chart
plt.figure(figsize=(10, 6))
plt.barh(top_df["pid_label"], top_df["count"], color='skyblue')
plt.xlabel("Count")
plt.ylabel("PID Label")
plt.title("Top 10 Most Frequent Predicates")
plt.gca().invert_yaxis()
plt.show()
plt.savefig('Top 10 Most Frequent Predicates')

# Pie Chart
plt.figure(figsize=(8, 8))
plt.pie(top_df["count"], labels=top_df["pid_label"], autopct='%1.1f%%', startangle=140, colors=plt.cm.Paired.colors)
plt.title("Distribution of Top 10 Predicates")
plt.show()
plt.savefig('Distribution of Top 10 Predicates')
