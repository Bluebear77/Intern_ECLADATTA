import pandas as pd
import numpy as np
from sklearn.metrics import confusion_matrix, precision_score, recall_score
import matplotlib.pyplot as plt

# Load the CSV file
file_path = 'manual - manual.csv'  # Update this path if your file is located elsewhere
data = pd.read_csv(file_path)

# Function to update conditions based on threshold
def update_conditions(threshold):
    conditions = []
    booleans = []

    for index, row in data.iterrows():
        actual = row['Actual condition']
        overall_similarity = row['overall_similarity']
        predicted = 'P' if overall_similarity >= threshold else 'N'
        conditions.append(predicted)
        
        if actual == 'P' and predicted == 'P':
            booleans.append('TP')
        elif actual == 'P' and predicted == 'N':
            booleans.append('FN')
        elif actual == 'N' and predicted == 'P':
            booleans.append('FP')
        elif actual == 'N' and predicted == 'N':
            booleans.append('TN')
    
    data['Predicted condition'] = conditions
    data['Boolean'] = booleans

# Define the threshold
threshold = 25

# Update conditions based on threshold
update_conditions(threshold)

# Save the updated CSV
updated_csv_path = 'updated_manual.csv'
data.to_csv(updated_csv_path, index=False)

# Generate confusion matrix
y_true = data['Actual condition'].map({'P': 1, 'N': 0})
y_pred = data['Predicted condition'].map({'P': 1, 'N': 0})
cm = confusion_matrix(y_true, y_pred)

# Precision and Recall
precision = precision_score(y_true, y_pred)
recall = recall_score(y_true, y_pred)

# Plot confusion matrix
plt.figure(figsize=(5, 5))
plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
plt.title('Confusion Matrix')
plt.colorbar()
tick_marks = np.arange(2)
plt.xticks(tick_marks, ['N', 'P'], rotation=45)
plt.yticks(tick_marks, ['N', 'P'])
plt.ylabel('True label')
plt.xlabel('Predicted label')

# Add text annotations
thresh = cm.max() / 2.
for i, j in np.ndindex(cm.shape):
    plt.text(j, i, format(cm[i, j], 'd'),
             ha="center", va="center",
             color="white" if cm[i, j] > thresh else "black")

plt.tight_layout()
conf_matrix_path = 'confusion_matrix.png'
plt.savefig(conf_matrix_path)

# Generate the report
report_content = f"""
# Classification Report

## Confusion Matrix
![Confusion Matrix](confusion_matrix.png)

## Precision and Recall
- **Precision**: {precision:.2f}
- **Recall**: {recall:.2f}
"""

report_path = 'report.md'
with open(report_path, 'w') as report_file:
    report_file.write(report_content)

print("Updated CSV, confusion matrix plot, and report have been generated.")
