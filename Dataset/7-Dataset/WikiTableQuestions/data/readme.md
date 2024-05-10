Here contains all files of the `WikiTableQuestions-1.0.2/data` directory.

`pull.py`: Extracts the table id and its origin file from each *.examples file and outputs a *.csv file.

Then the the origin file `csv/xxx-csv/yyy.csv` will be used as index to track the corresponding URL.


| Dataset                                         |
|-------------------------------------------------|
| ├── training (14152 examples)                   |
| ├── pristine-unseen-tables (4344 examples)     |
| ├── pristine-seen-tables (3537 examples)       |
| ├── random-split-1                             |
| │   ├── random-split-seed-1-train              |
| │   └── random-split-seed-1-test               |
| ├── random-split-2                             |
| │   ├── random-split-seed-2-train              |
| │   └── random-split-seed-2-test               |
| ├── random-split-3                             |
| │   ├── random-split-seed-3-train              |
| │   └── random-split-seed-3-test               |
| ├── ...                                        |
| ├── training-before300 (300 examples)           |
| └── annotated-all.examples (300 examples annotated with gold logical forms) |
