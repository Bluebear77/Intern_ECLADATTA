import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, precision_score, recall_score
import seaborn as sns

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

# Define the threshold
threshold = 25

# Update conditions based on the threshold
update_conditions(threshold)

# Save the updated CSV
updated_csv_path = 'updated_manual.csv'
data.to_csv(updated_csv_path, index=False)

# Calculate confusion matrix, precision, and recall
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

# Generate the report.md file
report_content = f"""
# Model Evaluation Report

## Confusion Matrix
![Confusion Matrix](confusion_matrix.png)

## Metrics
- **Precision:** {precision:.2f}
- **Recall:** {recall:.2f}

## Actual Condition Counts and Ratios
- **Total Positives (P):** {total_positives}
- **Total Negatives (N):** {total_negatives}
- **Positive Ratio:** {positive_ratio:.2f}
- **Negative Ratio:** {negative_ratio:.2f}
"""

with open('report.md', 'w') as report_file:
    report_file.write(report_content)

# Print the first 3 rows to verify the update
print(data.head(3))
