# 100 Business Instances Pre-Processing for ReasTAP Model

This repository contains the pre-processing pipeline for the 100 Business Instances, designed as input for the ReasTAP model. The final processed output is stored in the `P5` directory.

## Directory Structure and Processing Stages

### 1. Raw Data Overview
- **Directories**:
  - `Complete`: Contains pages where all tables were successfully extracted.
  - `Missing`: Contains pages that have tables in the original URL but none were extracted, due to issues like unparsed templates or regular table formats.
  - `NoTable`: Contains pages that do not have tables in the original URL.
  - `Raw`: Contains the original `_doc.json` files split per URL.

### 2. Data Extraction (Complete to P1)
- **Script**: `extract.py`
- **Description**: Extracts all related information from the complete dataset.

### 3. Structuring Input for ReasTAP (P1 to P2)
- **Script**: `formulate.py`
- **Description**: Builds the input structure necessary for the REASTAP implementation.

### 4. Column Types and Key Columns (P2 to P3)
- **Script**: `supply.py`
- **Description**: Determines the `"column_types"` and `"key_column"` using DAGOBAH annotations.

### 5. Refining Column Types (P3 to P4)
- **Script**: `rct.py`
- **Description**: Refines the column types to ensure accuracy and consistency in the data.

### 6. Handling Empty Date Values (P4 to P5)
- **Script**: `date.py`
- **Description**: Uses `9999` as a placeholder for empty date values in the `"date_column"`.

## Files and Directories

- `Complete/`: Directory containing fully extracted data pages.
- `Missing/`: Directory for pages with tables that were not extracted.
- `NoTable/`: Directory for pages without any tables.
- `Raw/`: Directory containing the original split JSON files.
- `P1/`, `P2/`, `P3/`, `P4/`, `P5/`: Directories representing different stages of data processing.
- `extract.py`: Script for initial data extraction from the complete dataset.
- `formulate.py`: Script for structuring input data for the REASTAP model.
- `supply.py`: Script for determining `"column_types"` and `"key_column"` using DAGOBAH.
- `rct.py`: Script for refining the column types.
- `date.py`: Script for handling empty date values by inserting placeholders.

## Final Output

The fully processed dataset is located in the `P5` directory, ready for input into the ReasTAP model.
