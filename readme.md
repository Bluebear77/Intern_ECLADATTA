# ECLADATTA Internship Project Documentation

This repo documents the results of an internship (March 2024 - August 2025) as part of the ECLADATTA project, which aims to improve the extraction and interpretation of latent knowledge from documents by analyzing both texts and tables.

## Background

**[ECLADATTA](https://ecladatta.github.io/)** (ExtraCtion of LAtent knowledge in Documents by conjointly Analyzing Texts and TAbles) is a project that explores the complementary nature of tables and text within or across documents. By leveraging both sources of information, the project aims to enhance data interpretation, quality assessment, and metadata enrichment, thereby boosting semantic services such as dataset indexing, question-answering systems, and knowledge base development.

## Contributions

- **Benchmark Analysis**: We conducted an analysis of publicly available benchmark datasets for reasoning over tables, with a focus on their interrelations and source URL comparison. This includes the recovery of QTSumm source URLs, with results available in the [recovery directory](https://github.com/Bluebear77/Intern_ECLADATTA/tree/main/7-Benchmark-Dataset/QTSumm/recovery).

  The CSV files containing each dataset's URLs can be found in the [csv directory](https://github.com/Bluebear77/Intern_ECLADATTA/tree/main/URL-Comparison/csv), and the overlap results are summarized in the [summary.csv file](https://github.com/Bluebear77/Intern_ECLADATTA/blob/main/URL-Comparison/csv/summary.csv).


- **Corpus Construction**: We constructed and studied three topic-specific corpora (female celebrities, business, telco) consisting of text and tables, pre-processed in both English and French.

- **ReasTAP Application**: We applied the ReasTAP model to generate a question-answer pairs (QAS) corpus requiring reasoning for the three created corpora. The outputs can be found at the following links:
  - [Business Corpus Output](https://github.com/Bluebear77/Intern_ECLADATTA/tree/main/ReasTAP/ReasTAP-main/synthetic_tableqa_generation/output-business)
  - [Celebrity Corpus Output](https://github.com/Bluebear77/Intern_ECLADATTA/tree/main/ReasTAP/ReasTAP-main/synthetic_tableqa_generation/output-celebrity)
  - [Telco Corpus Output](https://github.com/Bluebear77/Intern_ECLADATTA/tree/main/ReasTAP/ReasTAP-main/synthetic_tableqa_generation/output-telco)

- **Text-Table Relatedness Evaluation**: We evaluated the relatedness between textual sections and tables within the same Wikipedia page, using cosine similarity of SBERT embeddings between generated QAS and text data.

## Directory Structure

### 1. **[7-Benchmark-Dataset](https://github.com/Bluebear77/Intern_ECLADATTA/tree/main/7-Benchmark-Dataset)**
   - **Description**: Contains a comprehensive study of seven benchmark datasets, focusing on their interrelations and their role in training large language models (LLMs).
   - **Datasets**: Includes ToTTo, LOGICNLG, QTSumm, LOTNLG, FetaQA, WTQ, and F2WTQ.

### 2. **[ECLADATTA-3-Corpus](https://github.com/Bluebear77/Intern_ECLADATTA/tree/main/ECLADATTA-3-Corpus)**
   - **Description**: Contains three corpora constructed for the ECLADATTA project, focusing on business, telco, and female celebrities. Each corpus is processed and structured for input into the ReasTAP model.

### 3. **[ReasTAP](https://github.com/Bluebear77/Intern_ECLADATTA/tree/main/ReasTAP)**
   - **Description**: Contains the results of the ReasTAP experiment conducted on the three ECLADATTA corpora, including the generated QAS corpus.

### 4. **[Text-Table-Matching](https://github.com/Bluebear77/Intern_ECLADATTA/tree/main/Text-Table-Matching)**
   - **Description**: Contains scripts and data for evaluating the similarity between textual paragraphs and tables through generated Question-Answer (QA) pairs. This involves text extraction, cleaning, embedding creation, and similarity calculation.

### 5. **[URL-Comparison](https://github.com/Bluebear77/Intern_ECLADATTA/tree/main/URL-Comparison)**
   - **Description**: Contains scripts and files for processing, analyzing, and visualizing URL data from the seven benchmark datasets and the three ECLADATTA corpora.

### 6. **[ECLADATTA CorpusWalker.md](https://github.com/Bluebear77/Intern_ECLADATTA/tree/main/ECLADATTA%20CorpusWalker.md)**
   - **Description**: A quick start guide for using the ECLADATTA CorpusWalker tool, which aids in the extraction and processing of tables and text from documents.
