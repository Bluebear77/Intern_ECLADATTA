import os

# Define the directories
directories = ["business-100", "telco-100"]
subdirectories = ["Complete", "Missing", "NoTable", "Raw"]

# Function to count files in a given directory
def count_files(directory):
    return len(os.listdir(directory))

# Initialize a dictionary to store counts
stats = {dir: {subdir: 0 for subdir in subdirectories} for dir in directories}

# Iterate over each directory and subdirectory to count files
for dir in directories:
    for subdir in subdirectories:
        subdir_path = os.path.join(dir, subdir)
        if os.path.exists(subdir_path):
            stats[dir][subdir] = count_files(subdir_path)

# Generate stats.md file
with open("stats.md", "w") as f:
    f.write("# File Statistics\n\n")
    for dir, subdir_counts in stats.items():
        f.write(f"## {dir}\n")
        for subdir, count in subdir_counts.items():
            f.write(f"- **{subdir}**: {count} files\n")
        f.write("\n")

print("stats.md file generated successfully.")

