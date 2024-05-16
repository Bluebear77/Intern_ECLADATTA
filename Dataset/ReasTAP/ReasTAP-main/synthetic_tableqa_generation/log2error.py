import csv
import re

# Function to parse the log file
def parse_log(log_file):
    error_data = {}
    with open(log_file, 'r') as file:
        for line in file:
            match = re.match(r"Error generating question for template (.+) in file (.+): (.+)", line)
            if match:
                template = match.group(1)
                file_name = match.group(2)
                error_message = match.group(3)
                error_detail = f"{error_message} for template {template}"
                
                if file_name not in error_data:
                    error_data[file_name] = set()
                error_data[file_name].add(error_detail)
    return error_data

# Function to write the CSV file
def write_csv(error_data, csv_file):
    with open(csv_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["File Name", "Error Message"])
        
        total_errors = 0
        sorted_files = sorted(error_data.keys())  # Sort the files with errors
        for file_name in sorted_files:
            for error in error_data[file_name]:
                writer.writerow([file_name, error])
                total_errors += 1

        # Append statistical analysis
        writer.writerow([])
        writer.writerow(["Statistics"])
        writer.writerow(["Total Unique Errors", total_errors])
        writer.writerow(["Total Files with Errors", len(error_data)])

# Main function
def main():
    log_file = 'log.txt'
    csv_file = 'error.csv'
    
    error_data = parse_log(log_file)
    write_csv(error_data, csv_file)
    print(f"Error data written to {csv_file} with statistics appended.")

if __name__ == "__main__":
    main()
