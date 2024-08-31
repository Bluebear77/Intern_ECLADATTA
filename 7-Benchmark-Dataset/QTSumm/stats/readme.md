# Stats Directory

This directory contains scripts and output files for analyzing the QTSumm dataset, focusing on identifying unique and duplicate tables across different dataset splits.

## Files Overview

- **`duplicate.py`**: Identifies tables that appear in two or more dataset files (`dev`, `test`, `train`) and generates summaries in both Markdown (`tables_summary.md`) and JSON (`tables_summary.json`) formats.

- **`tables.py`**: Calculates the number of unique tables in each dataset split (`dev`, `test`, `train`) and the total number of unique tables across all three, outputting the results to `tables.txt`.

- **`tables.txt`**: A text file containing the count of unique tables in each dataset split and the combined total.

- **`tables_summary.json`**: A JSON file listing tables that appear in multiple dataset splits, including their IDs and sources.

- **`tables_summary.md`**: A Markdown file summarizing the tables that are duplicated across different dataset splits, formatted as a table for easy reference.
