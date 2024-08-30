# Script 

This directory contains scripts for format conversion and URL extraction related to various datasets.

## Scripts Overview

- **`json2csv.py`**: Converts JSON format files to CSV format.
- **`jsonl2csv.py`**: Converts JSONL format files to CSV format.
- **`pageID2title.py`**: Converts pageID values to page titles.
- **`title2pageID.py`**: Converts page titles to pageID values.
- **`id2url.py`**: Extracts the pageID from the `.csv` file name and constructs the corresponding URL.

## Special Purpose Script

- **`filter-invalid-ToTTo.py`**:  
  Filters out rows in a CSV where the Page ID URL ends with `"curid=-1"` and writes the remaining valid rows to a new file.

