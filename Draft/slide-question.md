### Can you prepare a zip file with all datasets: LOGICNLG, ToTTo, QTSumm with the tables in csv format?

**Here contains a zip file with all datasets: LOGICNLG, ToTTo, QTSumm with the tables in csv format:
https://drive.google.com/file/d/1PAwlg9wRPO-lg_rddVGWjIZ05airZLWD/view?usp=sharing**


<br/>
LOGICNLG originally in csv:https://github.com/wenhuchen/LogicNLG/blob/master/all_csv.zip<br/>
ToTTo  originally in jasonl:https://storage.googleapis.com/totto-public/totto_data.zip<br/>
QTSumm  originally  in jason:https://huggingface.co/datasets/yale-nlp/QTSumm/tree/main


### Can you prepare a spreadsheet showing for each dataset (LOGICNLG and ToTTo) the Wikipedia page from which the table comes from?

- LOGICNLG, ToTTo, and QTSumm Datasets in CSV Format:<br/>
https://drive.google.com/file/d/1PAwlg9wRPO-lg_rddVGWjIZ05airZLWD/view?usp=sharing

- Wikipedia Source Overview for LOGICNLG and ToTTo Datasets:<br/>
  https://docs.google.com/spreadsheets/d/1G619zqazyZBmOIQp54zqRC_kr0S9n1h4Z4UVngqYe9I/edit?usp=sharing<br/>

- Overlapped URLs for LOGICNLG and ToTTo Datasets:<br/>
  https://docs.google.com/spreadsheets/d/13peuRZqLMsJiddPEVT4v5Y-L5YbHPu3DON6Oitp3aI4/edit?usp=sharing<br/>
  In total 1428 overlapped URLs.

- LOGICNLG does **NOT** provide urls. 
 https://wenhuchen.github.io/logicnlg.github.io/<br/>
 <br/>They treat the table id as url.

 ![image](https://github.com/Bluebear77/Intern_ECLADATTA/assets/119409649/dd0d2694-7933-4021-8afa-452b82201403)
 
 
 LOGICNLG is based on Table-Fact-Checking by the same author Wenhu Chen, they only provide table id:
 <br/>https://github.com/wenhuchen/Table-Fact-Checking/tree/master/data
 
 ```
 all_csv: it contains all the table files in the csv format.
 
 all_csv_ids.json: it contains all the table ids
 ```

ToTTo: Title format URLs:
```
http://en.wikipedia.org/wiki/Title_of_the_Page
```

LOGICNLG: Page ID format URLs:
```
http://en.wikipedia.org/?curid=xxx
```


#### So I need to unify their format.

Use API:https://en.wikipedia.org/w/api.php

- 1st attempt:<br/>
  Convert ToTTo Title format URLs to Page ID format URLs.<br/>
  Results in 12619/136162, 9% invalid conversion.(Ones ends with "curid=-1")<br/>
 
- 2nd attempt:<br/>
  Convert LOGICNLG Page ID format URLs to Title format URLs.<br/>
  Results in 247/16573, 1.4% invalid conversion.
> Choose `Title format URLs`?

- Overview of LoTTo and LOGICNLG:<br/>
  https://docs.google.com/spreadsheets/d/1G619zqazyZBmOIQp54zqRC_kr0S9n1h4Z4UVngqYe9I/edit?usp=sharing


### Can you study the overlap between LOGICNLG and ToTTo in terms tables? And in terms of Wikipedia pages from which the tables come from? They extract 2000 tables from LOGICNLG and 2000 tables from ToTTO ... this makes 4k tables. But at the end, they have 2934 tables, so they through out some ... WHY? Because they overlap?


#### From Dataset:
1427 overlapped URLs: https://docs.google.com/spreadsheets/d/13peuRZqLMsJiddPEVT4v5Y-L5YbHPu3DON6Oitp3aI4/edit?usp=sharing


####  From paper:
- First they filter out the tables that are:
1) too large or too small
2) with only string-type columns
3) with hierarchical structures (e.g., containing more than onetable header)

Then they extract 2000 from each LOGICNLG and 2000 from ToTTo.

- De-biasing: Becasue there are many tables have similar content in LOGICNLG, **they keep only one table for each unique table header.** They did not mention ToTTo.

