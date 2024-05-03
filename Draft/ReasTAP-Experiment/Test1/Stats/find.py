import os
import re
import numpy as np

def rank_reasoning_skills(stats_dir):
    # Prepare the output file for results
    output_file = os.path.join(stats_dir, "find.md")
    
    # Open the output file
    with open(output_file, 'w') as output:
        output.write("# Ranking of Instances by Reasoning Types and Variance of Percentages\n\n")
        
        # Dictionary to store the number of reasoning types and their variances for each file
        reasoning_stats = {}

        # Regex patterns to find the number of reasoning types and percentages
        total_types_pattern = re.compile(r"Total (\d+) unique reasoning types are produced.")
        percentage_pattern = re.compile(r"Percentage = (\d+\.\d+)%")
        
        # Iterate over each markdown file in the directory
        for filename in os.listdir(stats_dir):
            if filename.startswith('stats_') and filename.endswith('.md') and not filename.endswith('all.md'):
                with open(os.path.join(stats_dir, filename), 'r') as file:
                    content = file.read()

                    total_match = total_types_pattern.search(content)
                    if total_match:
                        num_types = int(total_match.group(1))
                        percentages = [float(match.group(1)) for match in percentage_pattern.finditer(content)]
                        
                        # Calculate variance of the reasoning type percentages
                        variance = np.var(percentages) if percentages else 0
                        
                        # Extract the instance number from the filename
                        instance_num = int(filename.split('_')[1].split('.')[0])
                        reasoning_stats[instance_num] = (num_types, variance)
        
        # Sort instances first by the number of reasoning types (descending) and then by variance (ascending)
        sorted_reasoning = sorted(reasoning_stats.items(), key=lambda x: (-x[1][0], x[1][1]))
        
        # Write the ranking to the output file
        for rank, (instance, stats) in enumerate(sorted_reasoning, start=1):
            output.write(f"Rank {rank}: Instance {instance} with {stats[0]} reasoning types and variance {stats[1]:.2f}<br/>\n")

# Set the directory where markdown files are located to the current directory
stats_dir = "."

# Rank the reasoning skills across all stats markdown files
rank_reasoning_skills(stats_dir)
