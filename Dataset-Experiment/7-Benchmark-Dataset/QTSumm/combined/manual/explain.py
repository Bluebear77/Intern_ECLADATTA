import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, precision_score, recall_score
import numpy as np
import itertools

# Load the dataset
file_path = 'manual-verified.csv'  # Change this to your file path
df = pd.read_csv(file_path)


# Use the correct column name
boolean_col = 'Boolean'  # Adjust this if the column name is different in your CSV

# Calculate the counts of each category in the Boolean column
tp = df[boolean_col].value_counts().get('TP', 0)
tn = df[boolean_col].value_counts().get('TN', 0)
fp = df[boolean_col].value_counts().get('FP', 0)
fn = df[boolean_col].value_counts().get('FN', 0)

# Calculate Precision and Recall
precision = round(tp / (tp + fp), 2) if (tp + fp) > 0 else 0
recall = round(tp / (tp + fn), 2) if (tp + fn) > 0 else 0

# Create the confusion matrix
y_true = []
y_pred = []

for index, row in df.iterrows():
    if row[boolean_col] == 'TP':
        y_true.append(1)
        y_pred.append(1)
    elif row[boolean_col] == 'TN':
        y_true.append(0)
        y_pred.append(0)
    elif row[boolean_col] == 'FP':
        y_true.append(0)
        y_pred.append(1)
    elif row[boolean_col] == 'FN':
        y_true.append(1)
        y_pred.append(0)

conf_matrix = confusion_matrix(y_true, y_pred)

# Save the confusion matrix as an image
plt.figure(figsize=(6, 4))
plt.imshow(conf_matrix, cmap='Blues', alpha=0.7)
plt.title('Confusion Matrix')
plt.xlabel('Predicted')
plt.ylabel('Actual')

# Add text annotations to the confusion matrix
classes = ['Negative', 'Positive']
tick_marks = np.arange(len(classes))
plt.xticks(tick_marks, classes)
plt.yticks(tick_marks, classes)

thresh = conf_matrix.max() / 2.0
for i, j in itertools.product(range(conf_matrix.shape[0]), range(conf_matrix.shape[1])):
    plt.text(j, i, format(conf_matrix[i, j], 'd'),
             horizontalalignment="center",
             color="white" if conf_matrix[i, j] > thresh else "black")

plt.colorbar()
plt.tight_layout()
plt.savefig('confusion_matrix.png')  # Change this to your desired save path

# Generate explanation text
explanation_text = f"""
# Data Analysis Report

## Confusion Matrix
![Confusion Matrix](confusion_matrix.png)

## Metrics
- **Precision**: {precision}
- **Recall**: {recall}

## Explanation
The data provided consists of various articles with their respective titles and matched titles. Based on the Boolean column indicating True Positives (TP), True Negatives (TN), False Positives (FP), and False Negatives (FN), the precision and recall metrics have been calculated to an accuracy of two decimal points. The confusion matrix visualizes the actual versus predicted conditions, showcasing the performance of the classification.

- **Precision** is the ratio of correctly predicted positive observations to the total predicted positives.
- **Recall** is the ratio of correctly predicted positive observations to all observations in the actual class.

Both metrics indicate a balanced performance of the classification model.
"""

# Save the report to a markdown file
with open('report.md', 'w') as file:  # Change this to your desired save path
    file.write(explanation_text)
