import os

# Define the subdirectories
subdirectories = ["Complete", "Missing", "NoTable", "Raw"]
ignore_file = "scan.py"

# Function to get a set of file names in a directory, excluding the ignore_file
def get_file_set(directory):
    return set(f for f in os.listdir(directory) if f != ignore_file)

# Initialize dictionaries to store file sets
file_sets = {subdir: get_file_set(subdir) for subdir in subdirectories}

# Calculate the union of Complete, Missing, and NoTable
union_set = file_sets["Complete"].union(file_sets["Missing"], file_sets["NoTable"])

# Find the difference between Raw and the union set
missing_in_raw = union_set - file_sets["Raw"]
extra_in_raw = file_sets["Raw"] - union_set

# Find files that are duplicated across Complete, Missing, and NoTable
duplicated_files = [file for file in union_set if (
    (file in file_sets["Complete"]) + 
    (file in file_sets["Missing"]) + 
    (file in file_sets["NoTable"])
) > 1]

# Print results
if missing_in_raw:
    print("Files present in Complete, Missing, or NoTable but missing in Raw:")
    for file in missing_in_raw:
        print(file)
else:
    print("No files are missing in Raw.")

if extra_in_raw:
    print("\nFiles present in Raw but not in Complete, Missing, or NoTable:")
    for file in extra_in_raw:
        print(file)
else:
    print("No extra files in Raw.")

if duplicated_files:
    print("\nDuplicated files across Complete, Missing, and NoTable:")
    for file in duplicated_files:
        print(file)
else:
    print("No duplicated files across Complete, Missing, and NoTable.")

print("\nCheck completed.")
