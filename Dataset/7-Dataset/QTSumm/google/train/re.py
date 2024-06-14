import os

def rename_files():
    # Define the directory where the files are located
    directory = '.'  # Replace with the correct directory path
    
    # Loop through the range of file indices
    for i in range(1, 500):
        for extension in ['csv', 'json', 'txt']:
            old_name = f'qtsumm_test_chunk_{i}.{extension}'
            new_name = f'qtsumm_train_chunk_{i}.{extension}'
            
            old_path = os.path.join(directory, old_name)
            new_path = os.path.join(directory, new_name)
            
            # Check if the old file exists
            if os.path.exists(old_path):
                # Rename the file
                os.rename(old_path, new_path)
                print(f'Renamed: {old_path} to {new_path}')
            else:
                print(f'File not found: {old_path}')

if __name__ == "__main__":
    rename_files()
