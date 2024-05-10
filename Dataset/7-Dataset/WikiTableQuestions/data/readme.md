Here contains all files of the `WikiTableQuestions-1.0.2/data` directory.

`pull.py`: Extracts the table id and its origin file from each *.examples file and outputs a *.csv file.

`synthesis.py`: Iterates every row of *.csv file, use the source file column as an index to track the URL. It uses the "csv/xxx-csv/yyy.csv" as an index. Use "xxx-csv" to go to the '../url/xxx-page'directory. Then use "yyy.csv" finds "yyy.json". Then it reads the json file and extracts the table title and url. The final output is a new complete-xxx-tables.csv, with 4 columns: id,source file,table title and url.

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
