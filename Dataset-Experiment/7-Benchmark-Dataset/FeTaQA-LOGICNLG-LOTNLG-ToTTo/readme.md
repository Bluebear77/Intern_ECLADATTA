#### Source:

- LOGICNLG: https://github.com/wenhuchen/LogicNLG/blob/master/all_csv.zip

- LoTNLG: https://github.com/yale-nlp/LLM-T2T/tree/main/data/LoTNLG

- FeTaQA: https://github.com/Yale-LILY/FeTaQA/tree/main/data

- ToTTo: ` wget https://storage.googleapis.com/totto-public/totto_data.zip ` >> `unzip totto_data.zip`

URLs of each wikipedia page in each dataset are either directly provided or reconstructed from file names:
LOGICNLG and LOTNLG datasets use encoded pageID in file names, which can be used to reconstruct URLs.
WTQ and F2WTQ datasets directly provide the pageID URLs from the "url" field.
ToTTo and FeTaQA datasets' URLs are directly provided in the page title format, which needs to be converted into the pageID(curid=xxx) format.
All URLs are standardized into the pageID format for consistency across datasets.
For the QTSumm dataset, URL recovery is necessary as source URLs are not directly provided, i.e. we do not know from which Wikipedia page the tables come from
