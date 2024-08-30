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
                
                # Sorting the similarity table by descending order of similarity scores
                table_data['qas_i_table_j_num'] = table_data['qas_i_table_j'].apply(lambda x: int(x.split('_')[-1]))
                table_data = table_data.sort_values(by='qas_i_table_j_num').drop(columns=['qas_i_table_j_num'])
                
                # Extract section column names
                section_names = table_data.columns[1:]
                
                # Now, we will sort the sections based on the similarity score for each row (each table)
                def sort_row(row):
                    # Extract the table identifier
                    table_id = row[0]
                    # Extract the similarity scores (which are in the rest of the columns)
                    scores = row[1:].astype(float)  # Convert to float to ensure proper sorting
                    # Sort the sections and scores together in descending order by the scores
                    sorted_sections_scores = sorted(zip(section_names, scores), key=lambda x: x[1], reverse=True)
                    # Rebuild the row with sorted sections and scores
                    sorted_sections, sorted_scores = zip(*sorted_sections_scores)
                    # Return the reordered row, starting with the table identifier
                    return [table_id] + list(sorted_scores)

                # Apply the sorting function to each row of the DataFrame
                sorted_table_data = table_data.apply(sort_row, axis=1, result_type='expand')

                # Rename the columns to reflect the sorted section names (keeping the 'qas_i_table_j' as the first column)
                sorted_section_names = ['qas_i_table_j'] + [section for section, _ in sorted(zip(section_names, table_data.iloc[0, 1:].astype(float)), key=lambda x: x[1], reverse=True)]
                sorted_table_data.columns = sorted_section_names

                # Save the sorted table to a CSV file
                table_file_path = os.path.join(output_subdir, 'similarity_table_sorted.csv')
                sorted_table_data.to_csv(table_file_path, index=False)

                # Append the sorted data to the 'all_tables' list if needed
                all_tables.append(sorted_table_data)

                # Plot the sorted similarity table
                plt.figure(figsize=(12, 6))
                line_styles = ['-', '--', '-.', ':']
                for i, qas_file in enumerate(sorted(qas_files, key=lambda x: int(os.path.basename(x).split('_')[-1].split('.')[0]))):
                    qas_filename = os.path.basename(qas_file).split('.')[0]
                    scores = sorted_table_data.loc[sorted_table_data['qas_i_table_j'] == qas_filename].drop('qas_i_table_j', axis=1).values.flatten().tolist()
                    plt.plot(sorted_section_names[1:], scores, label=qas_filename, linestyle=line_styles[i % len(line_styles)])
                
                plt.xlabel('Sections (Sorted by Similarity)')
                plt.ylabel('Cosine Similarity')
                plt.title(f'Sorted Cosine Similarity Scores for QAS {qas_index}')
                plt.legend()
                plt.xticks(rotation=90)
                plt.tight_layout()
                plot_file_path = os.path.relpath(os.path.join(output_subdir, 'sorted_similarity_plot.png'), start=output_root)
                plt.savefig(os.path.join(output_subdir, 'sorted_similarity_plot.png'))
                plt.close()
                plot_files.append(plot_file_path)
    
    # Append plots to report.md
    report_path = os.path.join(output_root, 'report.md')
    with open(report_path, 'a') as report_file:  # Open in append mode
        for plot_file in plot_files:
            report_file.write(f"![Sorted Similarity Plot]({plot_file})\n\n")

if __name__ == "__main__":
    qas_root = './embedding/qas'
    text_root = './embedding/text/'
    output_root = './embedding/output/cosine'

    os.makedirs(output_root, exist_ok=True)
    process_directories(qas_root, text_root, output_root)
