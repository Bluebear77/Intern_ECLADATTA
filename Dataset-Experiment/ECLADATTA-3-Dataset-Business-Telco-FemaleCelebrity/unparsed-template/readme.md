# Unparsed Template 

This directory contains records of unparsed templates encountered during the CorpusWalker parsing of wikitables across various datasets. 

## Directory Structure

- **business-100/**: Contains records related to the business dataset.
- **celebrity-100/**: Contains records related to the celebrity dataset.
- **telco-100/**: Contains records related to the telco dataset.


## Contents

Each subdirectory (`business-100`, `celebrity-100`, `telco-100`) contains the following types of files:

- **`.txt` Files**: These files list the missing tables that were not parsed correctly.
- **`.csv` Files**: These files contain the extracted missing template names from the table content, providing insight into which templates caused parsing issues.
- **stats.py**: A script that analyzes the distribution of unparsed templates across all CSV files in the directory, generating a summary report and visualizations in the form of a pie chart and a bar chart.


## Purpose

The purpose of this directory is to record the unparsed templates in Wikipedia pages that were encountered during the CorpusWalker parsing process. This is particularly important because:

- **Template Format Issues**: Not all tables are marked with the expected `"class=*.+` format, making them difficult for automated parsers to identify.
- **Text Section Tables**: Many tables are embedded within the text sections of pages. These tables are often recognizable to humans but are challenging for computers to distinguish from regular text.

By documenting these instances, we aim to improve the parsing process and provide a reference for future improvements to table extraction algorithms.

