
Here is the Recovery QTSumm Dataset.

The QTSumm directory contains the recovery of source URL of the QTSumm dataset.  The final result is [qtsumm_dev.csv, qtsumm_test.csv, qtsumm_train.csv] in the combined directory.

Python scripts (google-find.py &  wiki-find.py ) are made to automate URL verification for the QTSumm dataset recovery by implementing a function that performs a fuzzy comparison of table content.

`google` directory contains the result of Google Search based on the 'table title + site:wikipedia.org' using google-find.py . There is a log.txt that stores the search and compare process.

`wiki-api` directory contains the result of Wiki-API based on the table title using wiki-find.py . There is a log.txt that stores the search and compare process.

`combined`  directory contains the result of the optimal selection result from both Google Search and Wiki-API based on the combined score.
`calculate_combined_score = int(0.7 * row['title_similarity'] + 0.3 * row['table_similarity'])`
More weights is given to the title because some table content could change by the time. 






***
From data:
- qtsumm_dev.json: 1052 tables
- qtsumm_train.json: 4981 tables
- qtsumm_test.json: 1078 tables
- Total number of tables in all .json files: 7111

From paper:
- 2,934 Tables from 2 sources: <br/>LOGICNLG (Chen et al., 2020a), 7,392 tables  <br/> ToTTo (Parikh et al., 2020), 83,141 tables

Source：
https://huggingface.co/datasets/yale-nlp/QTSumm/tree/main
