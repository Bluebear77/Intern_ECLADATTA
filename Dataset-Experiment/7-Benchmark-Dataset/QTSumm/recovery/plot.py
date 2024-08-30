import pandas as pd
import matplotlib.pyplot as plt

# Read the input files
files = ['qtsumm_dev.csv', 'qtsumm_train.csv', 'qtsumm_test.csv']
dataframes = [pd.read_csv(file) for file in files]

# Define distinct colors for the plots
colors = ['#1f77b4', '#ff7f0e', '#2ca02c']

# Create a figure for the plots
plt.figure(figsize=(14, 12))

# First plot: 3 curves, one for each file
plt.subplot(2, 1, 1)
for df, label, color in zip(dataframes, ['Dev', 'Train', 'Test'], colors):
    similarity_counts = df['overall_similarity'].value_counts().sort_index()
    plt.plot(similarity_counts.index, similarity_counts.values, label=label, linewidth=2, color=color)
plt.xlabel('Overall Similarity Score', fontsize=14)
plt.ylabel('Number of Occurrences', fontsize=14)
plt.title('Similarity Score Distribution per File', fontsize=16)
plt.legend(fontsize=12)
plt.grid(True)

# Second plot: 1 curve for all instances among all files
plt.subplot(2, 1, 2)
all_data = pd.concat(dataframes)
all_similarity_counts = all_data['overall_similarity'].value_counts().sort_index()
plt.plot(all_similarity_counts.index, all_similarity_counts.values, label='All Data', color='black', linewidth=2)
plt.xlabel('Overall Similarity Score', fontsize=14)
plt.ylabel('Number of Occurrences', fontsize=14)
plt.title('Overall Similarity Score Distribution', fontsize=16)
plt.legend(fontsize=12)
plt.grid(True)

# Save the plot to a file
plt.tight_layout()
plt.savefig('curve_refined.png')

# Create the Markdown content
markdown_content = """
# Similarity Score Distribution

## Plot 1: Distribution per File

![Plot 1](curve_refined.png)

## Plot 2: Overall Distribution

![Plot 2](curve_refined.png)
"""

# Write the Markdown content to a file
with open('curve_refined.md', 'w') as f:
    f.write(markdown_content)

print("Markdown file 'curve_refined.md' with the plots has been created.")
