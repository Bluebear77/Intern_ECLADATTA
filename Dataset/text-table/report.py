import os
import pandas as pd
import matplotlib.pyplot as plt

def process_csv(file_path):
    df = pd.read_csv(file_path)
    unique_qas_files = df['QAS_File'].unique()
    
    results = []
    for qas_file in unique_qas_files:
        subset = df[df['QAS_File'] == qas_file]
        highest_score = subset['Similarity'].max()
        average_score = subset['Similarity'].mean()
        results.append({
            'QAS_File': qas_file,
            'Highest_Similarity': highest_score,
            'Average_Similarity': average_score
        })
    
    return pd.DataFrame(results)

def generate_bar_chart(df, title, output_path):
    fig, ax = plt.subplots()
    bar_width = 0.35
    index = range(len(df))
    
    bars1 = plt.bar(index, df['Highest_Similarity'], bar_width, label='Highest Similarity')
    bars2 = plt.bar([i + bar_width for i in index], df['Average_Similarity'], bar_width, label='Average Similarity')
    
    plt.xlabel('QAS_File')
    plt.ylabel('Similarity Score')
    plt.title(title)
    plt.xticks([i + bar_width / 2 for i in index], df['QAS_File'], rotation=45, ha='right')
    plt.legend()
    
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close(fig)

def generate_overview_bar_chart(data, output_path):
    num_files = len(next(iter(data.values()))['QAS_File'].unique())
    fig, ax = plt.subplots(figsize=(num_files / 2, 8))

    combined_df = pd.DataFrame()
    for method, df in data.items():
        df['Method'] = method
        combined_df = pd.concat([combined_df, df], ignore_index=True)
    
    combined_df.sort_values(by='Average_Similarity', inplace=True)
    
    bar_width = 0.2
    x_ticks = combined_df['QAS_File'].unique()
    x_pos = list(range(len(x_ticks)))

    for i, method in enumerate(data.keys()):
        df = combined_df[combined_df['Method'] == method]
        df.sort_values(by='Average_Similarity', inplace=True)
        pos = [j + i * bar_width for j in range(len(df))]
        ax.bar(pos, df['Highest_Similarity'], width=bar_width, label=f'{method} Highest', alpha=0.5)
        ax.bar([p + bar_width for p in pos], df['Average_Similarity'], width=bar_width, label=f'{method} Average', alpha=0.5)

    plt.xlabel('QAS_File')
    plt.ylabel('Similarity Score')
    plt.title('Overview of Similarity Scores - Bars')
    plt.xticks([r + bar_width for r in range(len(x_ticks))], x_ticks, rotation=45, ha='right')
    plt.legend()
    
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close(fig)

def generate_overview_line_chart(data, output_path):
    num_files = len(next(iter(data.values()))['QAS_File'].unique())
    fig, ax = plt.subplots(figsize=(num_files / 2, 8))

    combined_df = pd.DataFrame()
    for method, df in data.items():
        df['Method'] = method
        combined_df = pd.concat([combined_df, df], ignore_index=True)
    
    combined_df.sort_values(by='Average_Similarity', inplace=True)
    
    x_ticks = combined_df['QAS_File'].unique()
    
    for method in data.keys():
        df = combined_df[combined_df['Method'] == method]
        df.sort_values(by='Average_Similarity', inplace=True)
        ax.plot(df['QAS_File'], df['Highest_Similarity'], label=f'{method} Highest', linestyle='-', marker='o')
        ax.plot(df['QAS_File'], df['Average_Similarity'], label=f'{method} Average', linestyle='--', marker='x')

    plt.xlabel('QAS_File')
    plt.ylabel('Similarity Score')
    plt.title('Overview of Similarity Scores - Lines')
    plt.xticks(range(len(x_ticks)), x_ticks, rotation=45, ha='right')
    plt.legend()
    
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close(fig)

# Other functions remain unchanged

def main():
    base_directories = ['./embedding/output/cosine', './embedding/output/jaccard']
    report_directory = './embedding/output/report'
    os.makedirs(report_directory, exist_ok=True)
    report_file = os.path.join(report_directory, 'report.md')
    
    combined_data = {
        'Cosine': pd.DataFrame(columns=['QAS_File', 'Highest_Similarity', 'Average_Similarity']),
        'Jaccard': pd.DataFrame(columns=['QAS_File', 'Highest_Similarity', 'Average_Similarity'])
    }

    with open(report_file, 'w') as report:
        for base_dir in base_directories:
            method = 'Cosine' if 'cosine' in base_dir else 'Jaccard'
            for root, dirs, files in os.walk(base_dir):
                for file in files:
                    if file.endswith('.csv'):
                        file_path = os.path.join(root, file)
                        title = f"Similarity Scores for {file}"
                        output_image_path = os.path.join(root, f"{file.replace('.csv', '')}.png")
                        
                        df = process_csv(file_path)
                        generate_bar_chart(df, title, output_image_path)
                        
                        if not df.empty:
                            combined_data[method] = pd.concat([combined_data[method], df], ignore_index=True)
                        
                        # Write to the report
                        relative_image_path = os.path.relpath(output_image_path, report_directory)
                        report.write(f"## {title}\n")
                        report.write(f"![{title}]({relative_image_path})\n\n")

    overview_bar_chart_path = os.path.join(report_directory, 'overview_similarity_bars.png')
    generate_overview_bar_chart(combined_data, overview_bar_chart_path)
    
    overview_line_chart_path = os.path.join(report_directory, 'overview_similarity_lines.png')
    generate_overview_line_chart(combined_data, overview_line_chart_path)

    combined_chart_path = os.path.join(report_directory, 'overview_similarity_combined.png')
    generate_combined_chart(combined_data, combined_chart_path)

    # Add these lines at the end of the main function to generate and write the summary table
    summary_df = generate_summary_table(combined_data)
    write_summary_table_to_report(summary_df, report_file)
    
    with open(report_file, 'a') as report:
        report.write(f"## Overview of Similarity Scores - Bars\n")
        report.write(f"![Overview of Similarity Scores - Bars](overview_similarity_bars.png)\n\n")
        report.write(f"## Overview of Similarity Scores - Lines\n")
        report.write(f"![Overview of Similarity Scores - Lines](overview_similarity_lines.png)\n\n")
        report.write(f"## Overview of Similarity Scores - Combined\n")
        report.write(f"![Overview of Similarity Scores - Combined](overview_similarity_combined.png)\n\n")

if __name__ == "__main__":
    main()
