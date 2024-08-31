# Google Directory

This directory contains the results and scripts related to the Google Search-based recovery process for the QTSumm dataset. The search is based on the query format: `wiki-page title + site:wikipedia.org`.

## Directory Structure

- **`dev/`**: Contains the split JSON files for the development set.
- **`test/`**: Contains the split JSON files for the test set.
- **`train/`**: Contains the split JSON files for the training set.
- **`script/`**: Contains the scripts used in the Google Search process.
- **`log.txt`**: Logs detailing the search and comparison processes.
- **`qtsumm_dev.csv`**: Recovered URLs for the development set.
- **`qtsumm_test.csv`**: Recovered URLs for the test set.
- **`qtsumm_train.csv`**: Recovered URLs for the training set.
- **`qtsumm_dev_sorted.csv`**: Sorted results for the development set based on similarity.
- **`qtsumm_test_sorted.csv`**: Sorted results for the test set based on similarity.
- **`qtsumm_train_sorted.csv`**: Sorted results for the training set based on similarity.

## Script Directory:

- **`google-track.py`**: Performs Google Search using the query format `wiki-page title + site:wikipedia.org` to recover potential URLs for each entry in the QTSumm dataset.
- **`sort.py`**: Sorts the recovered results (`qtsumm_dev.csv`, `qtsumm_test.csv`, `qtsumm_train.csv`) by the `overall_similarity` score in ascending order and outputs the sorted files.
- **`split.py`**: Splits the original JSON files into smaller JSON chunks, each containing 10 URLs, which are then organized into the `dev`, `test`, and `train` directories.
- **`convert.py`**: [Include a brief description if available; if not, leave it out.]

## Process Overview
1. **Splitting**:  
   The `split.py` script divides the original QTSumm JSON files into smaller, more manageable chunks, stored in the `dev`, `test`, and `train` directories.

2. **Google Search**:  
   The `google-track.py` script searches for Wikipedia pages using the `wiki-page title + site:wikipedia.org` format. The top results are logged and stored.

3. **Sorting**:  
   The `sort.py` script organizes the search results based on the `overall_similarity` score, creating sorted CSV files for easier analysis.


4. **Logging**:  
   All search and comparison processes are logged in `log.txt` for reference and troubleshooting.

