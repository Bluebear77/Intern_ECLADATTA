import pandas as pd

# Load the CSV file
file_path = 'manual.csv'  # Update this path as needed
data = pd.read_csv(file_path)

# Function to update conditions based on a defined threshold
def update_conditions(threshold):
    for index, row in data.iterrows():
        actual = row['Actual condition']
        overall_similarity = row['overall_similarity']
        
        # Use 'PP' for positive predictions and 'PN' for negative predictions
        predicted = 'PP' if overall_similarity >= threshold else 'PN'
        
        data.at[index, 'Predicted condition'] = predicted
        
        # Update 'Boolean' column based on actual and predicted conditions
        if actual == 'P' and predicted == 'PP':
            data.at[index, 'Boolean'] = 'TP'
        elif actual == 'P' and predicted == 'PN':
            data.at[index, 'Boolean'] = 'FN'
        elif actual == 'N' and predicted == 'PP':
            data.at[index, 'Boolean'] = 'FP'
        elif actual == 'N' and predicted == 'PN':
            data.at[index, 'Boolean'] = 'TN'

# Define the threshold
threshold = 25

# Update conditions based on the threshold
update_conditions(threshold)

# Save the updated CSV
updated_csv_path = 'updated_manual.csv'
data.to_csv(updated_csv_path, index=False)

# Print the first 3 rows to verify the update
print(data.head(3))
