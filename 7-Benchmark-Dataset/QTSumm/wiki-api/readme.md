# Wiki-API Directory

This directory contains the results and scripts related to the Wiki-API-based recovery process for the QTSumm dataset. The search is based on the wiki-page title using the MediaWiki API.

## Directory Structure

- **`qtsumm_dev.csv`**: Recovered URLs for the development set.
- **`qtsumm_dev_sorted.csv`**: Sorted results for the development set based on similarity.
- **`qtsumm_test.csv`**: Recovered URLs for the test set.
- **`qtsumm_test_sorted.csv`**: Sorted results for the test set based on similarity.
- **`qtsumm_train.csv`**: Recovered URLs for the training set.
- **`qtsumm_train_sorted.csv`**: Sorted results for the training set based on similarity.
- **`wiki-track.py`**: Script for recovering URLs using the Wiki-API.
- **`sort.py`**: Script for sorting the recovered results by overall similarity.
- **`log2.txt`**: Log file detailing the search and comparison processes.

## Script Descriptions

- **`wiki-track.py`**: Uses the MediaWiki API (`https://en.wikipedia.org/w/api.php`) to search for Wikipedia pages based on the wiki-page title, recovering potential URLs for each entry in the QTSumm dataset.

- **`sort.py`**: Sorts the recovered results (`qtsumm_dev.csv`, `qtsumm_test.csv`, `qtsumm_train.csv`) by the `overall_similarity` score in ascending order and outputs the sorted files.



## Process Overview

1. **Wiki-API Search**:  
   The `wiki-track.py` script searches for Wikipedia pages using the MediaWiki API based on the wiki-page title. The top results are logged and stored.

2. **Sorting**:  
   The `sort.py` script organizes the search results based on the `overall_similarity` score, creating sorted CSV files for easier analysis.

3. **Logging**:  
   All search and comparison processes are logged in `log2.txt` for reference and troubleshooting.

