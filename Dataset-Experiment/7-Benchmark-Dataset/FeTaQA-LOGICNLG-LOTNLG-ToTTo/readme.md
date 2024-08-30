# FeTaQA-LOGICNLG-LOTNLG-ToTTo Directory

This directory contains datasets and scripts related to URL extraction and conversion for various datasets.

## Directory Structure

- **FeTaQA**  
- **LOGICNLG**  
- **LOTNLG**  
- **ToTTo**  
- **Script**  

## Content Overview

### Dataset Directories (`FeTaQA`, `LOGICNLG`, `LOTNLG`, `ToTTo`)

Each of these directories contains a `.csv` file that includes the source URLs in the pageID format.

### Script Directory

The `Script` directory contains the code responsible for URL extraction and conversion.

## Source Links

- **LOGICNLG**: [Download all_csv.zip](https://github.com/wenhuchen/LogicNLG/blob/master/all_csv.zip)
- **LoTNLG**: [GitHub Repository](https://github.com/yale-nlp/LLM-T2T/tree/main/data/LoTNLG)
- **FeTaQA**: [GitHub Repository](https://github.com/Yale-LILY/FeTaQA/tree/main/data)
- **ToTTo**: [Download totto_data.zip](https://storage.googleapis.com/totto-public/totto_data.zip)

## URL Handling Details

- **LOGICNLG and LOTNLG**:  
  URLs are reconstructed from encoded pageIDs present in the file names.
  
- **WTQ and F2WTQ**:  
  URLs are directly provided in the "url" field as pageID URLs.
  
- **ToTTo and FeTaQA**:  
  URLs are provided in page title format, which requires conversion to the pageID (`curid=xxx`) format.

## Standardization

All URLs are standardized into the pageID format for consistency across datasets.

