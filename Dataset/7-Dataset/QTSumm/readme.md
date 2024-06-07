Here is the dataset of QTSumm.

- 2,934 Tables from 2 sources: <br/>LOGICNLG (Chen et al., 2020a), 7,392 tables  <br/> ToTTo (Parikh et al., 2020), 83,141 tables

Source：
https://huggingface.co/datasets/yale-nlp/QTSumm/tree/main

***

`google` directory contains the result of Google Search based on the 'table title + site:wikipedia.org'.

`wiki-api`  directory contains the result of Wiki-API ('https://en.wikipedia.org/w/api.php') based on the table title.

`cpombined` directory select the optimal result from both Google Search and  Wiki-API by calculate_combined_score = int(0.5 * row['title_similarity'] + 0.5 * row['table_similarity'])
.

