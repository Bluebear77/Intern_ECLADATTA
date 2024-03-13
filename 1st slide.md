# QTSUMM: Query-Focused Summarization over Tabular Data

## Questions:

- How many templates? 

  16

- Do we have the full list?

   Kind of. I find the question template of the ReasTAP. The summarizationo template of QTSUMM is based on ReasTAP, but it is not posted on github.
  
  https://github.com/Yale-LILY/ReasTAP/blob/main/synthetic_tableqa_generation/question_template.json

   
  https://github.com/Yale-LILY/ReasTAP/tree/main/synthetic_tableqa_generation/question_generator

 ![image](https://github.com/Bluebear77/Sailing_log/assets/119409649/4eed5961-4d22-4511-bb6b-a12776b615cf)


- How the template is chosen based on the query? Which case they apply?
  ![image](https://github.com/Bluebear77/Sailing_log/assets/119409649/538d5fcf-f14e-4f7a-9315-2773062d55e3)

 

  
```diff
- Code of refactor?
- No template found for the 
```
  

  







## Detailed roadmap:

### Template:
#### [QTSUMM: Query-Focused Summarization over Tabular Data]:"For each reasoning operation, the fact generator
(adopted from Zhao et al. (2022b)) takes a table and a query as input."
![image](https://github.com/Bluebear77/Sailing_log/assets/119409649/4983764e-294b-4232-9a4b-3890f1ad1119)

#### [REASTAP: Injecting Table Reasoning Skills During Pre-training via Synthetic Reasoning Examples] : " The
example generation pipeline was adapted from Yoran et al. (2021)" https://aclanthology.org/2022.emnlp-main.615.pdf
![image](https://github.com/Bluebear77/Sailing_log/assets/119409649/488b1959-34a7-4f02-ac03-fc14159a7368)

#### [Turning Tables: Generating Examples from Semi-structured Tables for Endowing Language Models with Reasoning Skills]：https://arxiv.org/pdf/2107.07261.pdf


![image](https://github.com/Bluebear77/Sailing_log/assets/119409649/8d8d18b4-1c70-4145-a894-8223fed6f306)


![image](https://github.com/Bluebear77/Sailing_log/assets/119409649/68cff967-a10b-40d0-9e43-d2ef6268f243)
" Approach overview. First, we use semi-structured tables to generate large amounts of data **from 16 different example generators (EGs)**, each corresponding to a different reasoning skill. Then, **a pre-trained LM is
trained over this data in a multi-task setup to obtain our model**, PReasM, where we dynamically sample examples
based on current model errors (arrow width corresponds to the number of sampled examples). Last, **our model is fine-tuned and evaluated on target tasks that require reasoning.**

We generate data by crawling tables from Wikipedia, and applying **16 different example generators (EGs)** on each table. Each EG corresponds to a particular reasoning skill (composition, numerical comparison, see Table 1 for full list), and **comprises a small set of question templates**,Variables in the templates are filled with content from the table, and the structure of the table allows to compute the answer automatically.

Each EG is associated with one or more question templates, which differ in their surface phrasing. Templates contain typed variables that are instantiated with content from the table (see all variables in Table 1)"

Me: It is used a pre-trained model and trained on given data setup, dynamically sample examples based on current model errors.

https://github.com/oriyor/turning_tables/blob/main/ExampleGeneration/ExampleGeneration/question_templates/tabreas_question_templates.json


![image](https://github.com/Bluebear77/Sailing_log/assets/119409649/08b0934a-dd85-4373-a5f6-c92a64c9b140)






### Refactor:
- [QTSUMM: Query-Focused Summarization over Tabular Data]:"We propose REFACTOR, which can retrieve and generate query-relevant facts from tables as intermediate results for model input (Zhou et al.,2022; Zhao et al., 2023b), mitigating the implicit reasoning processes of text generation models."
- 

***
# Investigating Table-to-Text Generation Capabilities of LLMs in Real-World Information Seeking Scenarios

## Questions:

  

Access of all datasets<br/>
List of the questions we had/ comes back to the template/ comparsion/ <br/>
examples with Logical Reasoning Type Definition/

  

### Datasets:
#### [Investigating Table-to-Text Generation Capabilities of LLMs in Real-World Information Seeking Scenarios]:
"LOTNLG and F2WTQ were constructed upon **the test set of LOGICNLG (Chen et al., 2020a) and WTQ (Pasupat and Liang, 2015) datasets**, which are publicly available under the licenses of MIT1 and CC BY-SA 4.02 , respectively. These licenses permit us to modify, publish, and distribute additional annotations upon the original dataset."

#### [Logical Natural Language Generation from Open-Domain Tables]:

https://aclanthology.org/2020.acl-main.708.pdf<br/>
https://github.com/wenhuchen/LogicNLG

To play with LogicNLG:https://wenhuchen.github.io/logicnlg.github.io/

The template LM file: https://github.com/wenhuchen/LogicNLG/tree/master/data
- The training/dev/test LM file
  The three files (train_lm, val_lm, test_lm) are used for training/testing all the models in the following format:
  ```
  {
    table_id: [ 
      [
        sent1,
        linked columns1,
        table title,
        template1
      ],
      [
        sent2,
        linked columns2,
        table title,
        template2
      ],
      ...
    ]
    table_id: [
      ...
    ]
  }
  ```
  The template sentence is generated by using entity linking file, which is not 100% accurate, it could miss some numbers or entities. Besides that, to accelerate the dataloading, we also preprocess the training file to have train_lm_preprocessed.json, which appends the "linearized table" in each sentence.
  

- The adversarial evaluation file
  These files (val_lm_pos_neg.json, test_lm_pos_neg.json) are used for adversarial evaluation, where each sentence is paired with an adversarial example with mild modification to test model's sensitivity against logic errors. The data is in the following format:
  ```
  {
    table_id: [ 
      {
        pos:[
          sent1,
          linked columns1,
          table title,
          template1        
        ]
        neg:[
          sent1-adv,
          linked columns1,
          table title,
          template1-adv        
        ]
      },
      {
        pos:[
          sent2,
          linked columns2,
          table title,
          template2  
        ]
        neg:[
          sent2-adv,
          linked columns2,
          table title,
          template2-adv
        ]    
      },
      ...
    ],
    table_id: [
      {
        ...
      },
      {
        ...    
      }
      ...
    ]
    ...
  }
  ```
  
#### LOGICNLG novelty:  

"We took their positive statements (the sentences which are entailed by the knowledge in the table) collected from "complex channel" (required to annotate sentences with logical inference) as our target text. To prevent confusion with the original dataset, **we name this table-to-text dataset as LOGICNLG, which contains 28,450 training, 4,260 validation, and 4,305 test examples based on 7,392 open-domain tables crawled from Wikipedia.** Each table has 5 different examples covering diverse types of logical inference."

  ![image](https://github.com/Bluebear77/Sailing_log/assets/119409649/5cfe5573-f1a2-4060-91c3-4b93a43e30cf)


"Involves very rich logical inference, every annotated sentence involves certain types of inference with minimum domain-specific knowledge. 

It is mainly composed of short sentences with **an average length of 11 and a simple syntactic structure, which isolates from other linguistic complexity to focus on the problem of logical inference**. 

The dataset contains tables with open schema crawled from diversified domains Figure 4. **The major categories are sports, politics, and entertainment.** The schema diversity of the tables make the rule-based system infeasible to apply. Besides, most of the tables have very rich numeral records, which provide a great testbed for logical inference"

#### [Compositional Semantic Parsing on Semi-Structured Tables]:

https://aclanthology.org/P15-1142.pdf


### Logical  reasoning operations:
#### [Investigating Table-to-Text Generation Capabilities of LLMs in Real-World Information Seeking Scenarios]:"To address this issue, application developers could tailor the table-to-text generation systems to generate multiple insights that encompass **different logical reasoning operations (Perlitz et al., 2022; Zhao et al., 2023b).**"

#### [Diversity Enhanced Table-to-Text Generation via Logic-Type Control]: 

https://arxiv.org/pdf/2205.10938.pdf

#### [Proceedings of the 17th Conference of the European Chapter of the Association for Computational Linguistics, pages 554–561
May 2-6, 2023 ©2023 Association for Computational LinguisticsLOFT: Enhancing Faithfulness and Diversity for Table-to-Text
Generation via Logic Form Control]:

https://aclanthology.org/2023.eacl-main.40.pdf<br/>
https://github.com/Yale-LILY/LoFT

