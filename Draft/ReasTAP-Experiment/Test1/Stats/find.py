import os
import re
from collections import Counter

def parse_markdown_stats(file_path):
    reasoning_type_counts = Counter()
    with open(file_path, 'r') as file:
        content = file.readlines()

    # Enhanced regex to capture reasoning type details correctly from formatted markdown
    pattern = re.compile(r"- \*\*(.+?)\*\*: Count = (\d+), Percentage = ([\d.]+)%")
    
    for line in content:
        match = pattern.search(line.strip())
        if match:
            reasoning_type = match.group(1)
            count = int(match.group(2))
            reasoning_type_counts[reasoning_type] = count

    return reasoning_type_counts

def calculate_diversity_score(reasoning_counts):
    types_count = len(reasoning_counts)
    # Calculate balance using entropy-like approach for simplicity
    if types_count > 0:
        total = sum(reasoning_counts.values())
        balance_score = sum((count / total) * ((count / total) * -1) for count in reasoning_counts.values())
        balance_score = -balance_score  # Normalize the balance score
    else:
        balance_score = 0  # No types found

    return types_count + balance_score  # Combine diversity and balance score

def rank_stats_files(directory):
    scores = []
    
    # Iterate over markdown files in the directory
    for filename in os.listdir(directory):
        if filename.startswith('stats_') and filename.endswith('.md'):
            file_path = os.path.join(directory, filename)
            reasoning_type_counts = parse_markdown_stats(file_path)
            score = calculate_diversity_score(reasoning_type_counts)
            scores.append((filename, score, reasoning_type_counts))
    
    # Sort files by score, highest first
    scores.sort(key=lambda x: x[1], reverse=True)
    
    # Print ranked list
    for idx, (filename, score, counts) in enumerate(scores):
        print(f"{idx + 1}. {filename} - Score: {score:.2f}, Reasoning Types: {len(counts)}, Distribution: {dict(counts)}")

# Specify the directory containing the markdown files
stats_directory = '.'

# Run the ranking function
rank_stats_files(stats_directory)
