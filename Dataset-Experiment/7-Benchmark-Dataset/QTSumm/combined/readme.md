# Combined Directory

This directory contains the final selection results combining both the Google Search and Wiki-API approaches for recovering the QTSumm dataset. The selection is based on the highest overall similarity score between both approaches.

## Directory Structure

- **`combined-result/`**: Contains the final combined results in the form of CSV files: 
  - `qtsumm_dev.csv`
  - `qtsumm_test.csv`
  - `qtsumm_train.csv`

- **`manual/`**: Contains human verification results for the 60 unique tables with the least overall similarity, selected from the development, test, and training sets.

- **`combine.py`**: Script for calculating the overall similarity score for each table, using the formula: `int(0.4 * row['title_similarity'] + 0.6 * row['table_similarity'])`. The script selects the table with the highest overall similarity from both approaches (Google Search and Wiki-API).

- **`manual.py`**: Script for selecting 20 unique tables with the least overall similarity from each set (development, test, and training), resulting in a total of 60 tables. These tables are used for further human verification.


## Process Overview

1. **Combining Results**:  
   The `combine.py` script evaluates the results from both the Google Search and Wiki-API methods by calculating the overall similarity score. The table with the highest score is selected as the optimal result for each entry.

2. **Final Output**:  
   The optimal results for the development, test, and training sets are saved in the `combined-result/` directory as `qtsumm_dev.csv`, `qtsumm_test.csv`, and `qtsumm_train.csv`.

3. **Manual Verification**:  
   The `manual.py` script identifies 60 unique tables with the lowest overall similarity scores (20 from each set). These tables are manually reviewed, and the results of this verification are stored 
