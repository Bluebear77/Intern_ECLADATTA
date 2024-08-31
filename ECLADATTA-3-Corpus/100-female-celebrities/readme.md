
# 100 Female Celebrities Pre-Processing for ReasTAP Model

This repository contains the pre-processing pipeline for the 100 Female Celebrities corpus, designed as input for the ReasTAP model. The final processed output is stored in the `P6` directory.

## Directory Structure and Processing Stages

### 1. Raw Data to Initial Extraction (P1)
- **Script**: `extract.py`
- **Description**: Extracts all related information from the raw data.

### 2. Structuring Input for ReasTAP (P1 to P2)
- **Script**: `formulate.py`
- **Description**: Builds the input structure necessary for the REASTAP implementation.

### 3. Column Types and Key Columns (P2 to P3)
- **Script**: `convert.py`
- **Description**: Determines the `"column_types"`, `"key_column"`, `"numeric_columns"`, and `"date_columns"` based on table information using regex. (Note: Should use DAGOBAH for better accuracy.)

### 4. Extracting Key Columns and Types (Raw to CSV)
- **Script**: `2JSON.py`
- **Description**: Extracts key columns and their types from DAGOBAH annotations in the raw JSON files and saves the results into CSV files.

### 5. DAGOBAH-based Column and Key Identification (P2 to P4)
- **Script**: `2JSON.py`
- **Description**: Determines `"column_types"` and `"key_column"` using DAGOBAH annotations.

### 6. Refining Column Types (P4 to P5)
- **Script**: `rct.py`
- **Description**: Refines the column types, ensuring that the number of rows in `"column_types"` matches the number of rows in `"header"`.

### 7. Handling Empty Date Values (P5 to P6)
- **Script**: `date.py`
- **Description**: Uses `9999` as a placeholder for empty date values in the `"date_column"`.

## Files and Directories
- `CSV/`: Directory containing CSV files generated from raw data.
- `Old/`: Directory for older versions of scripts or data.
- `P1/`, `P2/`, `P3/`, `P4/`, `P5/`, `P6/`: Directories representing different stages of data processing.
- `100-female-celebrities-v2.csv`: CSV file containing processed data.
- `2JSON.py`: Extracts typing labels and primary key information from JSON files, processes them against corresponding CSV files, and outputs updated JSON files along with logs of the processing.
- `convert.py`: Script for converting and processing data between stages.
- `date.py`: Script for handling date columns.
- `extract.py`: Script for initial data extraction.
- `formulate.py`: Script for structuring input data for REASTAP.
- `pcsv.py`:  Extracts typing labels and primary key information from JSON files, outputs them into corresponding CSV files, and logs any issues encountered during the extraction and processing.
- `rct.py`: Script for refining column types.
- `supply.py`: Directly extracts the "column_types","key_column" using DAGOBAH
- `type.csv`: CSV file containing column type definitions.
- `wikipedia_fr_personnalitesfeminines100_fr_cat.csv`: Source data file.
- `wikipedia_fr_personnalitesfeminines100_fr_stats.json`: JSON file with statistical data.

## Final Output

The fully processed dataset is located in the `P6` directory, ready for input into the ReasTAP model.
