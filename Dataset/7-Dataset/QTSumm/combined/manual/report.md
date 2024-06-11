
# Data Analysis Report

## Confusion Matrix
![Confusion Matrix](confusion_matrix.png)

## Metrics
- **Precision**: 0.86
- **Recall**: 0.86

## Explanation
## Explanation
The data provided consists of various articles with their respective titles and matched titles. The goal is to evaluate how well the method recovers the origin URL based on title matching. The Boolean column indicates True Positives (TP), True Negatives (TN), False Positives (FP), and False Negatives (FN).

- **True Positives (TP)**: Cases where the title matching correctly identifies the origin URL.
- **True Negatives (TN)**: Cases where the title matching correctly identifies non-matching titles.
- **False Positives (FP)**: Cases where the title matching incorrectly identifies a non-matching title as a match.
- **False Negatives (FN)**: Cases where the title matching fails to identify a matching title.

### Metrics
- **Precision**: The ratio of correctly predicted positive matches to the total predicted positive matches. A precision of 0.86 indicates that 86% of the URLs recovered as matches are correct.
- **Recall**: The ratio of correctly predicted positive matches to all actual matches. A recall of 0.86 indicates that 86% of the actual matching URLs were correctly identified by the title matching method.

Both precision and recall values indicate a balanced and effective performance of the title matching method in recovering the origin URLs.
