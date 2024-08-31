import pandas as pd

# List of input and output filenames
file_names = ['qtsumm_dev.csv', 'qtsumm_test.csv', 'qtsumm_train.csv']
output_files = ['qtsumm_dev_sorted.csv', 'qtsumm_test_sorted.csv', 'qtsumm_train_sorted.csv']

# Loop through each file, sort by 'overall_similarity', and save to new file
for input_file, output_file in zip(file_names, output_files):
    # Read the CSV file
    df = pd.read_csv(input_file)
    
    # Sort the DataFrame by 'overall_similarity' in ascending order
    df_sorted = df.sort_values(by='overall_similarity', ascending=True)
    
    # Save the sorted DataFrame to a new CSV file
    df_sorted.to_csv(output_file, index=False)

print("Files sorted and saved successfully.")
