# F2WTQ Dataset

This directory contains the scripts and files related to the URL extraction process of the F2WTQ Dataset.

## Files Overview

- **`*.json`**: The 3 original raw F2WTQ data files.
- **`complete-F2WTQ-*.csv`**: The URL extraction results corresponding to each JSON file.
- **`F2WTQ.csv`**: A compressed CSV file containing all URLs extracted from the 3 datasets.

## About F2WTQ

The F2WTQ dataset is constructed using the WTQ dataset (Pasupat and Liang, 2015) as a basis.

Source: [Yale NLP - LLM-T2T Project](https://github.com/yale-nlp/LLM-T2T/tree/main/data/F2WTQ)

## Script Descriptions

- **`find.py`**: Extracts URLs from the JSON files and generates the corresponding `complete-F2WTQ-*.csv` files.
- **`merge.py`**: Merges the 3 `complete-F2WTQ-*.csv` files into a single `F2WTQ.csv` file.

