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

def main():
    base_directories = ['./embedding/output/cosine', './embedding/output/jaccard']
    report_file = './embedding/output/report.md'
    
    with open(report_file, 'w') as report:
        for base_dir in base_directories:
            for root, dirs, files in os.walk(base_dir):
                for file in files:
                    if file.endswith('.csv'):
                        file_path = os.path.join(root, file)
                        title = f"Similarity Scores for {file}"
                        output_image_path = file_path.replace('.csv', '.png')
                        
                        df = process_csv(file_path)
                        generate_bar_chart(df, title, output_image_path)
                        
                        # Write to the report
                        report.write(f"## {title}\n")
                        report.write(f"![{title}]({output_image_path})\n\n")

if __name__ == "__main__":
    main()
