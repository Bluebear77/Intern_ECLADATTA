Here is the dataset of QTSumm.

- 2,934 Tables from 2 sources: <br/>LOGICNLG (Chen et al., 2020a), 7,392 tables  <br/> ToTTo (Parikh et al., 2020), 83,141 tables

Source：
https://huggingface.co/datasets/yale-nlp/QTSumm/tree/main

***
```
{
    "example_id": "{example_id_placeholder}",
    "table": {
        "title": "{table_title_placeholder}",
        "table_id": "{table_id_placeholder}",
        "header": ["{header1_placeholder}", "{header2_placeholder}", "...", "{headerN_placeholder}"],
        "rows": [
            ["{row1_data1_placeholder}", "{row1_data2_placeholder}", "...", "{row1_dataN_placeholder}"],
            ["{row2_data1_placeholder}", "{row2_data2_placeholder}", "...", "{row2_dataN_placeholder}"],
            "...",
            ["{rowM_data1_placeholder}", "{rowM_data2_placeholder}", "...", "{rowM_dataN_placeholder}"]
        ]
    },
    "query": "{query_placeholder}",
    "summary": "{summary_placeholder}",
    "row_ids": [{row_index_placeholder}]
}

```

---
license: mit
task_categories:
- text-generation
- summarization
- table-question-answering
---
# QTSumm Dataset
The **QTSumm** dataset is a large-scale dataset for the task of **query-focused summarization over tabular data**. 
It contains 7,111 human-annotated query-summary pairs over 2,934 tables covering diverse topics. 
To solve this task, a text generation system has to perform **human-like reasoning and analysis** over the given table to generate a tailored summary. 

## Citation
```
@misc{zhao2023qtsumm,
      title={QTSumm: Query-Focused Summarization over Tabular Data}, 
      author={Yilun Zhao and Zhenting Qi and Linyong Nan and Boyu Mi and Yixin Liu and Weijin Zou and Simeng Han and Ruizhe Chen and Xiangru Tang and Yumo Xu and Arman Cohan and Dragomir Radev},
      year={2023},
      eprint={2305.14303},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
```

