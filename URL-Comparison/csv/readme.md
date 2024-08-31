# CSV Directory Documentation

This directory contains various CSV files that records its dataset's source URL and the comparison result.

## Files and Descriptions

### Dataset Files

- **Name-cleaned.csv**
  - **Description**: Contains the unique URLs in each dataset after cleaning and deduplication processes.
  - **Examples**:
    - `F2WTQ-cleaned.csv`: Cleaned unique URLs from the F2WTQ dataset.
    - `FeTaQA-cleaned.csv`: Cleaned unique URLs from the FeTaQA dataset.
    - `LOGICNLG-cleaned.csv`: Cleaned unique URLs from the LOGICNLG dataset.
    - `LOTNLG-cleaned.csv`: Cleaned unique URLs from the LOTNLG dataset.
    - `ToTTo-cleaned.csv`: Cleaned unique URLs from the ToTTo dataset.
    - `WTQ-cleaned.csv`: Cleaned unique URLs from the WTQ dataset.

- **Name.csv**
  - **Description**: Contains every URL found in each dataset, including duplicates and uncleaned entries.
  - **Examples**:
    - `F2WTQ.csv`: All URLs from the F2WTQ dataset.
    - `FeTaQA.csv`: All URLs from the FeTaQA dataset.
    - `LOGICNLG.csv`: All URLs from the LOGICNLG dataset.
    - `LOTNLG.csv`: All URLs from the LOTNLG dataset.
    - `ToTTo.csv`: All URLs from the ToTTo dataset.
    - `WTQ.csv`: All URLs from the WTQ dataset.

### ECLADATTA Files

- **business100.csv**
  - **Description**: Contains URLs specific to the business corpus used in the ECLADATTA project.

- **female100.csv**
  - **Description**: Contains URLs specific to the female celebrities corpus used in the ECLADATTA project.

- **female100_english.csv**
  - **Description**: Contains URLs specific to the English version of the female celebrities corpus.

- **telco100.csv**
  - **Description**: Contains URLs specific to the telecommunications corpus used in the ECLADATTA project.

### Summary Files

- **summary.csv**
  - **Description**: Contains the overlap results across all datasets, showing the common URLs that appear in multiple datasets.
