import os
import shutil

# Define the directories
raw_dir = "../Raw"
no_table_dir = "../NoTable"
complete_dir = "../Complete"
current_dir = "."

# Get a set of all files in NoTable and Complete directories
no_table_files = set(os.listdir(no_table_dir))
complete_files = set(os.listdir(complete_dir))

# Combine the sets to have all excluded files
excluded_files = no_table_files.union(complete_files)

# Get all files in the Raw directory
raw_files = set(os.listdir(raw_dir))

# Filter out the files that are in excluded_files
files_to_copy = raw_files.difference(excluded_files)

# Copy the remaining files to the current directory
for file in files_to_copy:
    source = os.path.join(raw_dir, file)
    destination = os.path.join(current_dir, file)
    shutil.copy(source, destination)
    print(f"Copied {file} to {current_dir}")

print("Copying completed.")
