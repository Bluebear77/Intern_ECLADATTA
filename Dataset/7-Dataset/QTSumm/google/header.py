# Open the original log file
with open('log.txt', 'r') as log_file:
    lines = log_file.readlines()

# Define the row ranges
dev_end = 28166
test_end = 56387

# Split the lines into the respective files
dev_lines = lines[:dev_end + 1]
test_lines = lines[dev_end + 1:test_end + 1]
train_lines = lines[test_end + 1:]

# Write to dev-log.txt
with open('dev-log.txt', 'w') as dev_file:
    dev_file.writelines(dev_lines)

# Write to test-log.txt
with open('test-log.txt', 'w') as test_file:
    test_file.writelines(test_lines)

# Write to train-log.txt
with open('train-log.txt', 'w') as train_file:
    train_file.writelines(train_lines)

print("Logs have been successfully split into dev-log.txt, test-log.txt, and train-log.txt.")
