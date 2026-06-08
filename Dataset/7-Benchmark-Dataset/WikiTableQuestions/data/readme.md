Here contains all files of the `WikiTableQuestions-1.0.2/data` directory.

`pull.py`: Extracts the table id and its origin file from each *.examples file and outputs a *.csv file.

`synthesis.py`: Iterates every row of *.csv file, use the source file column as an index to track the URL. It uses the "csv/xxx-csv/yyy.csv" as an index. Use "xxx-csv" to go to the '../url/xxx-page'directory. Then use "yyy.csv" finds "yyy.json". Then it reads the json file and extracts the table title and url. The final output is a new complete-xxx-tables.csv, with 4 columns: id,source file,table title and url.

Then the the origin file `csv/xxx-csv/yyy.csv` will be used as index to track the corresponding URL.

***
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
