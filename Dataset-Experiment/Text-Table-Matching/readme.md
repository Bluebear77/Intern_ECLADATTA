# Text-Table-Matching Directory

This directory contains scripts and data used to evaluate the similarity between textual paragraphs and tables through generated Question-Answer (QA) pairs. The process involves text extraction, cleaning, embedding creation, and similarity calculation.

## Directory Structure

- **`business5/`**: Contains 5 sample files from the business corpus of the matching experiment.
- **`celebrity5/`**: Contains 5 sample files from the female celebrity corpus of the matching experiment.
- **`input-file/`**: Contains the extracted QA pairs and text sections used in the matching process.

## Scripts Overview

- **`para.py`**: Extracts text from the `instance_i.json` files.
- **`clean.py`**: Cleans the extracted text by removing wiki markup and other unnecessary elements.
- **`qs.py`**: Extracts QA pairs from the `synthetic_qa_output_instance_i_v6.json` files.
- **`embedding.py`**: Creates Sentence-BERT (SBERT) embeddings for each paragraph of the wiki pages and the QA pairs associated with the same table.
- **`cosine.py`**: Calculates the cosine similarity between the text paragraph embeddings and QA pair embeddings.
- **`report.py`**: Generates reports and plots based on the calculated similarity scores.

## Background

### Idea:
This project evaluates how closely a paragraph of text relates to a table by generating textual representations of tables through Question-Answer pairs (QAs). The similarity between these QAs and textual paragraphs is assessed using cosine similarity, calculated between SBERT embeddings of the paragraphs and QA pairs.

### Methodology:

1. **Selection**:  
   - Select 5 pages from the celebrity corpus.

2. **Extraction**:  
   - Extract all text and QA sets from each Wiki page into text files. Clean the extracted text and QAs using NLP techniques (text in French, QAs in English).

3. **Create Embeddings**:  
   - Generate SBERT embeddings using the `sentence-transformers/paraphrase-multilingual-mpnet-base-v2` model for each paragraph and QA set, producing 768-dimensional vector embeddings.

4. **Calculate Similarity**:  
   - Compute the cosine similarity between the embeddings of all text paragraphs and each QA set within the same wiki page.

### Goal:
The objective is to assess the relevance of textual paragraphs to associated tables by analyzing the similarity scores between them. This similarity is then used to evaluate potential matches between the paragraphs and the tables.

