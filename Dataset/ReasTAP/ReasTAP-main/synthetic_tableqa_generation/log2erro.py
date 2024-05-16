def process_log_file(log_file_path, error_file_path):
    unique_errors = set()
    error_counts = {}

    # Read the log file and process errors
    with open(log_file_path, 'r') as log_file:
        for line in log_file:
            if line not in unique_errors:
                unique_errors.add(line)
            if line in error_counts:
                error_counts[line] += 1
            else:
                error_counts[line] = 1

    # Write unique errors to error.txt
    with open(error_file_path, 'w') as error_file:
        for error in unique_errors:
            error_file.write(error)

    # Print statistical analysis
    total_errors = sum(error_counts.values())
    unique_error_count = len(unique_errors)
    most_common_error = max(error_counts, key=error_counts.get)
    most_common_error_count = error_counts[most_common_error]

    print(f"Total errors: {total_errors}")
    print(f"Unique errors: {unique_error_count}")
    print(f"Most common error: {most_common_error.strip()}")
    print(f"Occurrences of most common error: {most_common_error_count}")

# Define paths
log_file_path = 'log.txt'
error_file_path = 'error.txt'

# Process the log file
process_log_file(log_file_path, error_file_path)

