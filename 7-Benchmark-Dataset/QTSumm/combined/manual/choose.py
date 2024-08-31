import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, precision_score, recall_score
import seaborn as sns
import numpy as np

# Load the CSV file
file_path = 'manual.csv'  # Update this path as needed
data = pd.read_csv(file_path)

# Remove any trailing spaces in column names
data.columns = data.columns.str.strip()

# Function to update conditions based on a defined threshold
def update_conditions(threshold):
    new_predicted_conditions = []
    for index, row in data.iterrows():
        actual = row['Actual condition']
        overall_similarity = row['overall_similarity']
        
        # Use 'P' for positive predictions and 'N' for negative predictions
        predicted = 'P' if overall_similarity >= threshold else 'N'
        new_predicted_conditions.append(predicted)
        
        # Update 'Boolean' column based on actual and predicted conditions
        if actual == 'P' and predicted == 'P':
            data.at[index, 'Boolean'] = 'TP'
        elif actual == 'P' and predicted == 'N':
            data.at[index, 'Boolean'] = 'FN'
        elif actual == 'N' and predicted == 'P':
            data.at[index, 'Boolean'] = 'FP'
        elif actual == 'N' and predicted == 'N':
            data.at[index, 'Boolean'] = 'TN'

    # Assign new predictions to the correct 'Predicted condition' column
    data['Predicted condition'] = new_predicted_conditions

# Evaluate model for thresholds from 20 to 40 and store precision and recall
thresholds = range(20, 41)
precisions = []
recalls = []

for threshold in thresholds:
    update_conditions(threshold)
    actual_conditions = data['Actual condition']
    predicted_conditions = data['Predicted condition']
    precision = precision_score(actual_conditions, predicted_conditions, pos_label='P')
    recall = recall_score(actual_conditions, predicted_conditions, pos_label='P')
    precisions.append(precision)
    recalls.append(recall)

# Find the intersection point
intersection_threshold = None
intersection_value = None

# Loop through thresholds to find the intersection
for i in range(1, len(thresholds)):
    if precisions[i-1] < recalls[i-1] and precisions[i] >= recalls[i]:
        # Linear interpolation to find the intersection point
        x1, y1 = thresholds[i-1], precisions[i-1]
        x2, y2 = thresholds[i], precisions[i]
        x3, y3 = thresholds[i-1], recalls[i-1]
        x4, y4 = thresholds[i], recalls[i]

        precision_slope = (y2 - y1) / (x2 - x1)
        recall_slope = (y4 - y3) / (x4 - x3)

        intersection_threshold = (y3 - y1 + precision_slope * x1 - recall_slope * x3) / (precision_slope - recall_slope)
        intersection_value = y1 + precision_slope * (intersection_threshold - x1)
        break

# Print the intersection point if found
if intersection_threshold is not None and intersection_value is not None:
    print(f'Intersection Point: Threshold={intersection_threshold:.2f}, Value={intersection_value:.2f}')

# Plot Precision and Recall vs. Threshold
plt.figure(figsize=(10, 7))
plt.plot(thresholds, precisions, label='Precision', marker='o')
plt.plot(thresholds, recalls, label='Recall', marker='o')
plt.xlabel('Threshold Overall Similarity Value')
plt.ylabel('Precision and Recall Value')
plt.title('Precision and Recall vs. Threshold')
plt.legend()
plt.grid(True)
plt.savefig('precision_recall_vs_threshold.png')
plt.close()

# Define the threshold for final update and reporting
threshold = 33.48
update_conditions(threshold)

# Calculate confusion matrix, precision, and recall for the final threshold
actual_conditions = data['Actual condition']
predicted_conditions = data['Predicted condition']
cm = confusion_matrix(actual_conditions, predicted_conditions, labels=['P', 'N'])
precision = precision_score(actual_conditions, predicted_conditions, pos_label='P')
recall = recall_score(actual_conditions, predicted_conditions, pos_label='P')

# Plot the confusion matrix
plt.figure(figsize=(10, 7))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=['P', 'N'], yticklabels=['P', 'N'])
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('Confusion Matrix')
plt.savefig('confusion_matrix.png')
plt.close()

# Calculate actual condition counts and ratios
total_positives = actual_conditions.value_counts().get('P', 0)
total_negatives = actual_conditions.value_counts().get('N', 0)
total_conditions = len(actual_conditions)
positive_ratio = total_positives / total_conditions
negative_ratio = total_negatives / total_conditions

# Add intersection point to the report if found
if intersection_threshold is not None and intersection_value is not None:
    intersection_report = f"""
## Intersection Point
- **Threshold:** {intersection_threshold:.2f}
- **Precision and Recall Value:** {intersection_value:.2f}
"""
else:
    intersection_report = "\n## Intersection Point\n- No intersection found\n"

# Generate the report.md file
report_content = f"""
# Model Evaluation Report

## Confusion Matrix
![Confusion Matrix](confusion_matrix.png)

## Precision and Recall vs. Threshold
![Precision and Recall vs. Threshold](precision_recall_vs_threshold.png)

## Metrics
- **Precision:** {precision:.2f}
- **Recall:** {recall:.2f}

## Actual Condition Counts and Ratios
- **Total Positives (P):** {total_positives}
- **Total Negatives (N):** {total_negatives}
- **Positive Ratio:** {positive_ratio:.2f}
- **Negative Ratio:** {negative_ratio:.2f}

{intersection_report}
"""

with open('report.md', 'w') as report_file:
    report_file.write(report_content)

# Print the first 3 rows to verify the update
# print(data.head(3))
