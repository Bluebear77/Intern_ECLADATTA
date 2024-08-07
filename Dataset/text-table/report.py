import os
import pandas as pd
import matplotlib.pyplot as plt
import json

def process_csv(file_path):
    df = pd.read_csv(file_path)
    # Check if the 'QAS_File' column exists
    if 'QAS_File' not in df.columns:
        print(f"Warning: 'QAS_File' column not found in {file_path}")
        return pd.DataFrame()  # Return an empty DataFrame if column not found

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
    combined_df = pd.concat(data, ignore_index=True)
    combined_df.sort_values(by='Average_Similarity', inplace=True)
    
    num_files = len(combined_df['QAS_File'].unique())
    fig, ax = plt.subplots(figsize=(num_files / 2, 8))

    bar_width = 0.2
    x_ticks = combined_df['QAS_File'].unique()
    x_pos = list(range(len(x_ticks)))

    ax.bar(x_pos, combined_df['Highest_Similarity'], width=bar_width, label='Highest Similarity', alpha=0.5)
    ax.bar([p + bar_width for p in x_pos], combined_df['Average_Similarity'], width=bar_width, label='Average Similarity', alpha=0.5)

    plt.xlabel('QAS_File')
    plt.ylabel('Similarity Score')
    plt.title('Overview of Cosine Similarity Scores - Bars')
    plt.xticks([r + bar_width / 2 for r in range(len(x_ticks))], x_ticks, rotation=45, ha='right')
    plt.legend()

    plt.tight_layout()
    plt.savefig(output_path)
    plt.close(fig)

def generate_overview_line_chart(data, output_path):
    combined_df = pd.concat(data, ignore_index=True)
    combined_df.sort_values(by='Average_Similarity', inplace=True)
    
    num_files = len(combined_df['QAS_File'].unique())
    fig, ax = plt.subplots(figsize=(num_files / 2, 8))

    x_ticks = combined_df['QAS_File'].unique()

    ax.plot(combined_df['QAS_File'], combined_df['Highest_Similarity'], label='Highest Similarity', linestyle='-', marker='o')
    ax.plot(combined_df['QAS_File'], combined_df['Average_Similarity'], label='Average Similarity', linestyle='--', marker='x')

    plt.xlabel('QAS_File')
    plt.ylabel('Similarity Score')
    plt.title('Overview of Cosine Similarity Scores - Lines')
    plt.xticks(range(len(x_ticks)), x_ticks, rotation=45, ha='right')
    plt.legend()

    plt.tight_layout()
    plt.savefig(output_path)
    plt.close(fig)

def generate_combined_chart(data, output_path):
    combined_df = pd.concat(data, ignore_index=True)
    combined_df.sort_values(by='Average_Similarity', inplace=True)
    
    num_files = len(combined_df['QAS_File'].unique())
    fig, ax = plt.subplots(figsize=(num_files / 2, 8))

    bar_width = 0.2
    x_ticks = combined_df['QAS_File'].unique()
    x_pos = list(range(len(x_ticks)))

    ax.bar(x_pos, combined_df['Highest_Similarity'], width=bar_width, label='Highest Similarity (Bar)', alpha=0.5)
    ax.bar([p + bar_width for p in x_pos], combined_df['Average_Similarity'], width=bar_width, label='Average Similarity (Bar)', alpha=0.5)

    ax.plot(combined_df['QAS_File'], combined_df['Highest_Similarity'], label='Highest Similarity (Line)', linestyle='-', marker='o')
    ax.plot(combined_df['QAS_File'], combined_df['Average_Similarity'], label='Average Similarity (Line)', linestyle='--', marker='x')

    plt.xlabel('QAS_File')
    plt.ylabel('Similarity Score')
    plt.title('Overview of Cosine Similarity Scores - Combined')
    plt.xticks([r + bar_width / 2 for r in range(len(x_ticks))], x_ticks, rotation=45, ha='right')
    plt.legend()

    plt.tight_layout()
    plt.savefig(output_path)
    plt.close(fig)

def generate_summary_table(data):
    summary_data = {
        'QAS_File': [],
        'Average Cosine': [],
        'Highest Cosine': [],
        'Median Cosine': []
    }

    combined_df = pd.concat(data, ignore_index=True)
    overall_avg_cosine = combined_df['Average_Similarity'].mean()
    overall_highest_cosine = combined_df['Highest_Similarity'].max()
    overall_median_cosine = combined_df['Average_Similarity'].median()

    summary_data['QAS_File'].append('All')
    summary_data['Average Cosine'].append(overall_avg_cosine)
    summary_data['Highest Cosine'].append(overall_highest_cosine)
    summary_data['Median Cosine'].append(overall_median_cosine)

    for qas_file in combined_df['QAS_File'].unique():
        cosine_subset = combined_df[combined_df['QAS_File'] == qas_file]

        summary_data['QAS_File'].append(qas_file)
        summary_data['Average Cosine'].append(cosine_subset['Average_Similarity'].mean() if not cosine_subset.empty else 'N/A')
        summary_data['Highest Cosine'].append(cosine_subset['Highest_Similarity'].max() if not cosine_subset.empty else 'N/A')
        summary_data['Median Cosine'].append(cosine_subset['Average_Similarity'].median() if not cosine_subset.empty else 'N/A')

    return pd.DataFrame(summary_data)

def write_summary_table_to_report(summary_df, report_file):
    with open(report_file, 'a') as report:
        report.write(f"## Summary Table\n")
        report.write(summary_df.to_markdown(index=False))
        report.write("\n\n")

def write_summary_table_to_csv(summary_df, output_csv_path):
    summary_df.to_csv(output_csv_path, index=False)

def generate_additional_table(report_directory, report_file):
    additional_table_data = {
        'instance_name': [],
        'nr of tables': [],
        'nr of paragraphs': [],
        'nr of comparisons': [],
        'URL': []
    }

    input_json_directory = './fr-multilingual-mpnet-base-v2/5-sample/input-json'
    for instance_file in os.listdir(input_json_directory):
        if instance_file.endswith('.json'):
            instance_path = os.path.join(input_json_directory, instance_file)

            with open(instance_path, 'r') as file:
                data = json.load(file)
                url = data['_source']['identificationMetadata']['url'][0]

            instance_id = instance_file.split('_')[-1].split('.')[0]
            qas_dir = f'./qas/qas_{instance_id}'
            text_dir = f'./text/v2/instance_{instance_id}'

            if os.path.exists(qas_dir):
                nr_of_tables = len(os.listdir(qas_dir))
            else:
                nr_of_tables = 0

            if os.path.exists(text_dir):
                nr_of_paragraphs = len(os.listdir(text_dir))
            else:
                nr_of_paragraphs = 0

            nr_of_comparisons = nr_of_tables * nr_of_paragraphs

            additional_table_data['instance_name'].append(f'instance_{instance_id}')
            additional_table_data['nr of tables'].append(nr_of_tables)
            additional_table_data['nr of paragraphs'].append(nr_of_paragraphs)
            additional_table_data['nr of comparisons'].append(nr_of_comparisons)
            additional_table_data['URL'].append(url)

    additional_table_df = pd.DataFrame(additional_table_data)
    additional_table_path = os.path.join(report_directory, 'additional_table.csv')
    additional_table_df.to_csv(additional_table_path, index=False)

    with open(report_file, 'a') as report:
        report.write(f"## Additional Table\n")
        report.write(additional_table_df.to_markdown(index=False))
        report.write("\n\n")

def main():
    base_directory = './embedding/output/cosine'
    report_directory = './embedding/output/report'
    os.makedirs(report_directory, exist_ok=True)
    report_file = os.path.join(report_directory, 'report.md')

    combined_data = []

    with open(report_file, 'w') as report:
        for root, dirs, files in os.walk(base_directory):
            for file in files:
                if file == 'cosine_similarity.csv':  # Check for specific file name
                    file_path = os.path.join(root, file)
                    title = f"Similarity Scores for {os.path.basename(root)}"
                    output_image_path = os.path.join(root, f"{os.path.basename(root)}.png")

                    df = process_csv(file_path)
                    generate_bar_chart(df, title, output_image_path)

                    if not df.empty:
                        combined_data.append(df.dropna())

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

    # Generate and write the summary table
    summary_df = generate_summary_table(combined_data)
    write_summary_table_to_report(summary_df, report_file)

    # Write summary table to a separate CSV file
    summary_csv_path = os.path.join(report_directory, 'summary_table.csv')
    write_summary_table_to_csv(summary_df, summary_csv_path)

    with open(report_file, 'a') as report:
        report.write(f"## Overview of Similarity Scores - Bars\n")
        report.write(f"![Overview of Cosine Similarity Scores - Bars](overview_similarity_bars.png)\n\n")
        report.write(f"## Overview of Similarity Scores - Lines\n")
        report.write(f"![Overview of Cosine Similarity Scores - Lines](overview_similarity_lines.png)\n\n")
        report.write(f"## Overview of Similarity Scores - Combined\n")
        report.write(f"![Overview of Cosine Similarity Scores - Combined](overview_similarity_combined.png)\n\n")

    # Generate and write the additional table
    generate_additional_table(report_directory, report_file)

if __name__ == "__main__":
    main()
