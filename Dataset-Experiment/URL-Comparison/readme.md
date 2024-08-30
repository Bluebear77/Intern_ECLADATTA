# URL-Comparison Directory

This directory contains scripts and files for processing, analyzing, and visualizing URL data from various datasets.

## Directory Structure

- **`csv/`**: Contains CSV files with URL data for various datasets.

- **`scripts/`**: Contains all Python scripts used for processing and analyzing the URL data.

- **`venn/`**: Contains Venn diagram visualizations for URL comparisons across datasets.

## Files Overview

- **`scripts/check.py`**: Removes duplicate URLs from each CSV file and saves the cleaned data as `*-cleaned.csv` in the `csv/` directory.

- **`scripts/venn.py`**: Generates Venn diagrams to compare the overlap of URLs between different datasets.

- **`scripts/count.py`**: Counts the total and unique URLs in both original and cleaned CSV files across datasets.

- **`scripts/female.py`**: Converts URLs from the French version of Wikipedia to their English equivalents.

- **`scripts/sdifference.py`**: Generates a bar chart comparing total URLs to unique URLs after cleaning, with results saved as a PNG file.

- **`stats.md`**: A markdown file summarizing URL statistics and analysis.

- **`stats.txt`**: A text file containing detailed statistics about the URLs in the datasets.

- **`url_comparison_chart.png`**: A chart comparing the distribution of URLs across datasets.

- **`url_comparison_chart_log_scale.png`**: A log-scale version of the URL comparison chart for better visualization of differences.

- **`url_counts_per_dataset.png`**: A chart displaying the count of URLs per dataset.
