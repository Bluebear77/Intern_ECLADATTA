
This directory contains scripts and files related to processing the `WikiTableQuestions-1.0.2/data` directory.

## Files Overview

- **`pull.py`**:  
  Extracts the table ID and its corresponding source file from each `*.examples` file and outputs the results into a `*.csv` file.

- **`synthesis.py`**:  
  Iterates through each row of the generated `*.csv` file to match table IDs with their URLs. The script uses the `source file` column as an index to locate the correct URL:
  
  1. **File Indexing**:  
     - The `source file` is formatted as `"csv/xxx-csv/yyy.csv"`.
     - The `"xxx-csv"` part is used to navigate to the `../url/xxx-page` directory.
     - The `"yyy.csv"` part is used to find the corresponding `"yyy.json"` file.

  2. **URL Extraction**:  
     - The script reads the `yyy.json` file to extract the table title and URL.
     - The final output is a new `complete-xxx-tables.csv` file containing four columns: `id`, `source file`, `table title`, and `url`.

- **URL Tracking**:  
  The original file (`csv/xxx-csv/yyy.csv`) is used as an index to track the corresponding URL.


**Dataset Splits:** 

We split 22033 examples into multiple sets:

- `training`:
  Training data (14152 examples)

- `pristine-unseen-tables`:
  Test data -- the tables are *not seen* in training data (4344 examples)

- `pristine-seen-tables`:
  Additional data where the tables are *seen* in training data. (3537 examples)
  (Initially intended to be used as development data, this portion of the
  dataset has not been used in any experiment in the paper.)

- `random-split-*`:
  For development, we split `training.tsv` into random 80-20 splits.
  Within each split, tables in the training data (`random-split-seed-*-train`)
  and the test data (`random-split-seed-*-test`) are disjoint.

- `training-before300`:
  The first 300 training examples.

- `annotated-all.examples`:
  The first 300 training examples annotated with gold logical forms.

For our ACL 2015 paper:

- In development set experiments:
  we trained on `random-split-seed-{1,2,3}-train`
  and tested on `random-split-seed-{1,2,3}-test`, respectively.

- In test set experiments:
  we trained on `training` and tested on `pristine-unseen-tables`.

**Supplementary Files:**

- `*.examples` files:
  The LispTree format of the dataset is used internally in our
  [SEMPRE](http://nlp.stanford.edu/software/sempre/) code base.
  The `*.examples` files contain the same information as the TSV files.
