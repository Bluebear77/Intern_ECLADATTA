# Benchmark Datasets Study

This directory contains a comprehensive study of seven benchmark datasets, with a focus on their interrelations.



### Datasets

1. **ToTTo**  
   A controlled table-to-text generation dataset.  
   [GitHub Repository](https://github.com/google-research-datasets/ToTTo)

2. **LOGICNLG**  
   A dataset for logical natural language generation from tables.  
   [Download CSV](https://github.com/wenhuchen/LogicNLG/blob/master/all_csv.zip)

3. **QTSumm**  
   A dataset for query-focused summarization over tabular data, created by integrating LOGICNLG and ToTTo with fact templates.  
   [Hugging Face Dataset](https://huggingface.co/datasets/yale-nlp/QTSumm)

4. **LOTNLG**  
   A logical table-to-text generation dataset based on LOGICNLG.  
   [GitHub Repository](https://github.com/yale-nlp/LLM-T2T/tree/main/data)

5. **FetaQA**  
   A factual table-based question answering dataset built on ToTTo.  
   [GitHub Repository](https://github.com/Yale-LILY/FeTaQA/tree/main/data)

6. **WTQ (WikiTableQuestions)**  
   A dataset for answering questions using tables from Wikipedia.  
   [Hugging Face Dataset](https://huggingface.co/datasets/wikitablequestions) | [GitHub Repository](https://github.com/ppasupat/WikiTableQuestions/tree/master/csv)

7. **F2WTQ**  
   An enhanced version of WTQ, focusing on factuality and logical consistency.  
   [GitHub Repository](https://github.com/yale-nlp/LLM-T2T/tree/main/data)

## Key Insights

- **QTSumm**: Developed by combining LOGICNLG and ToTTo, QTSumm implements a fact template approach to generate query-focused summaries over tabular data.
  
- **Training LLMs**: Datasets such as LOGICNLG, LOTNLG, FetaQA, and F2WTQ are instrumental in training various large language models, helping to advance the field of natural language generation and understanding from tabular data.

## Purpose

This directory serves as a resource for researchers and practitioners seeking to explore the intricacies of these datasets, their contributions to LLM training, and their impact on the development of advanced table-to-text and summarization models.
