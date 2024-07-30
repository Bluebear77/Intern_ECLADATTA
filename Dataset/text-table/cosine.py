import os
import glob
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import cosine_similarity
from tqdm import tqdm

def read_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def calculate_cosine_similarity(text1, text2):
    vector1 = np.array([float(num) for num in text1.split()])
    vector2 = np.array([float(num) for num in text2.split()])
    return cosine_similarity([vector1], [vector2])[0][0]

def process_directories(qas_root, text_root, output_root):
    qas_dirs = glob.glob(os.path.join(qas_root, 'qas_*'))
    all_tables = []
    plot_files = []
    for qas_dir in tqdm(qas_dirs, desc="Processing QAS Directories"):
        qas_index = os.path.basename(qas_dir).split('_')[1]
        text_dir = os.path.join(text_root, f'instance_{qas_index}')
        if os.path.exists(text_dir):
            qas_files = glob.glob(os.path.join(qas_dir, '*.txt'))
            text_files = glob.glob(os.path.join(text_dir, '*.txt'))
            output_data = []
            table_data = pd.DataFrame(columns=['qas_i_table_j'] + [f'section_{os.path.basename(text_file).split("_")[1].split(".")[0]}' for text_file in text_files])
            for qas_file in tqdm(qas_files, desc=f"Processing files in {qas_dir}", leave=False):
                qas_text = read_file(qas_file)
                qas_filename = os.path.basename(qas_file).split('.')[0]
                row_data = {'qas_i_table_j': qas_filename}
                for text_file in text_files:
                    text_content = read_file(text_file)
                    similarity = calculate_cosine_similarity(qas_text, text_content)
                    text_filename = f'section_{os.path.basename(text_file).split("_")[1].split(".")[0]}'
                    row_data[text_filename] = similarity
                    output_data.append([similarity, qas_filename, text_filename])
                
                row_df = pd.DataFrame([row_data])
                table_data = pd.concat([table_data, row_df], ignore_index=True)
            
            if output_data:
                output_subdir = os.path.join(output_root, f'qas_{qas_index}')
                os.makedirs(output_subdir, exist_ok=True)

                # Sort and save cosine_similarity.csv
                df = pd.DataFrame(output_data, columns=['Similarity', 'QAS_File', 'Text_File'])
                df['QAS_File_num'] = df['QAS_File'].apply(lambda x: int(x.split('_')[-1]))
                df = df.sort_values(by='QAS_File_num').drop(columns=['QAS_File_num'])
                output_file_path = os.path.join(output_subdir, 'cosine_similarity.csv')
                df.to_csv(output_file_path, index=False)
                
                # Sort and save similarity_table.csv
                table_data['qas_i_table_j_num'] = table_data['qas_i_table_j'].apply(lambda x: int(x.split('_')[-1]))
                table_data = table_data.sort_values(by='qas_i_table_j_num').drop(columns=['qas_i_table_j_num'])
                table_file_path = os.path.join(output_subdir, 'similarity_table.csv')
                table_data.to_csv(table_file_path, index=False)
                all_tables.append(table_data)

                # Plot
                plt.figure(figsize=(12, 6))
                line_styles = ['-', '--', '-.', ':']
                for i, qas_file in enumerate(sorted(qas_files, key=lambda x: int(os.path.basename(x).split('_')[-1].split('.')[0]))):
                    qas_filename = os.path.basename(qas_file).split('.')[0]
                    scores = table_data.loc[table_data['qas_i_table_j'] == qas_filename].drop('qas_i_table_j', axis=1).values.flatten().tolist()
                    plt.plot(sorted(table_data.columns[1:], key=lambda x: int(x.split('_')[-1])), scores, label=qas_filename, linestyle=line_styles[i % len(line_styles)])
                plt.xlabel('Paragraphs')
                plt.ylabel('Cosine Similarity')
                plt.title(f'Cosine Similarity Scores for QAS {qas_index}')
                plt.legend()
                plt.xticks(rotation=90)
                plt.tight_layout()
                plot_file_path = os.path.join(output_subdir, 'similarity_plot.png')
                plt.savefig(plot_file_path)
                plt.close()
                plot_files.append(plot_file_path)
    
    # Append plots to report.md
    report_path = os.path.join(output_root, 'report.md')
    with open(report_path, 'a') as report_file:  # Open in append mode
        for plot_file in plot_files:
            report_file.write(f"![Similarity Plot]({plot_file})\n\n")

if __name__ == "__main__":
    qas_root = './embedding/qas'
    text_root = './embedding/text'
    output_root = './embedding/output/report'

    os.makedirs(output_root, exist_ok=True)
    process_directories(qas_root, text_root, output_root)
