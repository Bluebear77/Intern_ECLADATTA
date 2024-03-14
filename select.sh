#!/bin/bash

# File path
FILE_PATH="$(pwd)/2024_03_14_13_18_09.json"

# Output file path for the selected subset
OUTPUT_FILE_PATH="$(pwd)/selected_subset.json"


# Temporary file for shuffled lines
TEMP_FILE=$(mktemp)

# Ensure temporary file gets deleted on exit
trap 'rm -f "$TEMP_FILE"' EXIT

# Shuffle randomly the lines in the file
shuf "$FILE_PATH" > "$TEMP_FILE"

# Use jq to filter and select first 100 instances, assuming each line is a valid JSON object
# Save the selected instances to the new JSON file. Adjust the jq filter as needed.
head -n 100 "$TEMP_FILE" | jq '.' > "$OUTPUT_FILE_PATH"


