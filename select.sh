#!/bin/bash

# File path
FILE_PATH="$(pwd)/2024_03_14_13_18_09.json"

# Output file path for the selected subset
OUTPUT_FILE_PATH="$(pwd)/selected_subset.json"


# Temporary file for shuffled lines
TEMP_FILE=$(mktemp)

# Ensure temporary file gets deleted on exit
trap 'rm -f "$TEMP_FILE"' EXIT

# Shuffle the lines in the file and select the first 100
shuf "$FILE_PATH" > "$TEMP_FILE"

# Use jq to filter and select the instances, assuming each line is a valid JSON object
# Save the selected instances to the new JSON file. Adjust the jq filter as needed.
head -n 100 "$TEMP_FILE" | jq '.' > "$OUTPUT_FILE_PATH"


# Note: You'll need to replace the jq '.' part with your actual criteria for selecting the instances you're interested in.
# For example, it might be something like 'select(.gender == "female")' depending on your JSON structure.
