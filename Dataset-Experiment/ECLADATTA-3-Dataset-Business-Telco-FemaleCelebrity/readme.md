# ECLADATTA-3 Corpus: Business, Telco, and Female Celebrities

This repository contains 3 corpora constructed for the ECLADATTA project.

## Directory Structure

- **100-female-celebrities/**: Contains the pre-processing pipeline for the 100 Female Celebrities dataset, designed for input into the ReasTAP model.
- **business-100/**: Contains the pre-processing pipeline for the 100 Business Instances dataset, designed for input into the ReasTAP model.
- **business-100/**: Contains the pre-processing pipeline for the 100 Telecommunication Instances dataset, designed for input into the ReasTAP model.
- **csv/**: Contains URL summarization CSV files for the 100 Female Celebrities, Business, and Telco corpus.
- **origin-files/**: Contains the original, unprocessed files used as input for the data processing pipelines.
- **unparsed-template/**: Contains records of unparsed templates encountered during the CorpusWalker parsing of wikitables, with a focus on documenting templates that were difficult to parse due to their format or location within the text.

- **stas.py**: A script that counts the number of files in specific subdirectories ("Complete," "Missing," "NoTable," and "Raw") within the "business-100" and "telco-100" directories. It generates a `stats.md` file summarizing the file counts.


## Usage

1. **Data Pre-processing**: Use the scripts within each specific directory (`100-female-celebrities`, `business-100`, `telco-100`) to process and prepare the data for analysis or model input.
2. **Unparsed Templates**: Refer to the `unparsed-template` directory to understand and analyze instances where Wikipedia tables were not correctly parsed.
3. **Statistics Generation**: Run the `stas.py` script to generate a summary of the file counts across different subdirectories, which is useful for tracking data processing progress.

