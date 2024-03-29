# QTSUMM: Query-Focused Summarization over Tabular Data

## Questions:

- How many templates? 

  16

- Do we have the full list?

   Kind of. I find the question template of the ReasTAP. The summarization template of QTSUMM is based on ReasTAP, but it is not posted on github.
  
  https://github.com/Yale-LILY/ReasTAP/blob/main/synthetic_tableqa_generation/question_template.json

   
  https://github.com/Yale-LILY/ReasTAP/tree/main/synthetic_tableqa_generation/question_generator
![image](https://github.com/Bluebear77/Intern_ECLADATTA/assets/119409649/5c490bf5-ba2c-4c6e-ba53-9f24a4f96a55)



- How the template is chosen based on the query? Which case they apply?
![image](https://github.com/Bluebear77/Intern_ECLADATTA/assets/119409649/be6756b4-85c8-4420-8f35-831f9927af6b)


 

  
```diff
- Code of refactor?
- I contacted the author Yilun Zhao asking for their code and got replied. He mentioned it is done by another author, he said he will ask him during the week.

```
  

  







## Detailed roadmap:

### Template:
#### [QTSUMM: Query-Focused Summarization over Tabular Data]:"For each reasoning operation, the fact generator
(adopted from Zhao et al. (2022b)) takes a table and a query as input."
![image](https://github.com/Bluebear77/Intern_ECLADATTA/assets/119409649/478a2192-98cc-4f5a-8b2c-34c2af6317bd)



#### [REASTAP: Injecting Table Reasoning Skills During Pre-training via Synthetic Reasoning Examples] : " The
example generation pipeline was adapted from Yoran et al. (2021)" https://aclanthology.org/2022.emnlp-main.615.pdf
![image](https://github.com/Bluebear77/Intern_ECLADATTA/assets/119409649/2e1b8821-53da-4243-9947-c5ca0ff74402)


#### [Turning Tables: Generating Examples from Semi-structured Tables for Endowing Language Models with Reasoning Skills]：https://arxiv.org/pdf/2107.07261.pdf


![image](https://github.com/Bluebear77/Intern_ECLADATTA/assets/119409649/8a498c54-2605-4373-8a35-e0557e121529)



![image](https://github.com/Bluebear77/Intern_ECLADATTA/assets/119409649/19a5c921-83fe-423a-98b9-551ba11f0272)

" Approach overview. First, we use semi-structured tables to generate large amounts of data **from 16 different example generators (EGs)**, each corresponding to a different reasoning skill. Then, **a pre-trained LM is
trained over this data in a multi-task setup to obtain our model**, PReasM, where we dynamically sample examples
based on current model errors (arrow width corresponds to the number of sampled examples). Last, **our model is fine-tuned and evaluated on target tasks that require reasoning.**

We generate data by crawling tables from Wikipedia, and applying **16 different example generators (EGs)** on each table. Each EG corresponds to a particular reasoning skill (composition, numerical comparison, see Table 1 for full list), and **comprises a small set of question templates**,Variables in the templates are filled with content from the table, and the structure of the table allows to compute the answer automatically.

Each EG is associated with one or more question templates, which differ in their surface phrasing. Templates contain typed variables that are instantiated with content from the table (see all variables in Table 1)"

Me: It is used a pre-trained model and trained on given data setup, dynamically sample examples based on current model errors.

https://github.com/oriyor/turning_tables/blob/main/ExampleGeneration/ExampleGeneration/question_templates/tabreas_question_templates.json

![image](https://github.com/Bluebear77/Intern_ECLADATTA/assets/119409649/576c7c5c-c526-4d72-ad0f-5daa9ed0254a)







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

_In its github,  no template is found for the table insight extraction._

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

![image](https://github.com/Bluebear77/Intern_ECLADATTA/assets/119409649/d11d6754-cd47-4278-8a4b-5ef5a5b04739)



"Involves very rich logical inference, every annotated sentence involves certain types of inference with minimum domain-specific knowledge. 

It is mainly composed of short sentences with **an average length of 11 and a simple syntactic structure, which isolates from other linguistic complexity to focus on the problem of logical inference**. 

The dataset contains tables with open schema crawled from diversified domains Figure 4. **The major categories are sports, politics, and entertainment.** The schema diversity of the tables make the rule-based system infeasible to apply. Besides, most of the tables have very rich numeral records, which provide a great testbed for logical inference"

#### [Compositional Semantic Parsing on Semi-Structured Tables]:

https://aclanthology.org/P15-1142.pdf <br/>
https://paperswithcode.com/dataset/wikitablequestions <br/>
play with the WikiTableQuestions :https://ppasupat.github.io/WikiTableQuestions/ <br/>
detailed experiment: https://worksheets.codalab.org/worksheets/0xf26cd79d4d734287868923ad1067cf4c/<br/>
The WTQ dataset, https://github.com/percyliang/sempre

The paper:


![image](https://github.com/Bluebear77/Intern_ECLADATTA/assets/119409649/cad35227-1e88-460a-b071-e278c82b1784)

SEMPRE:

SEMPRE is a toolkit that makes it easy to develop semantic parsers for new tasks. The main paradigm is to learn a feature-rich discriminative semantic parser from a set of utterance-denotation pairs. One can also quickly prototype rule-based systems, learn from other forms of supervision, and combine any of the above.

A semantic parser maps natural language utterances into an intermediate logical
form, which is "executed" to produce a denotation that is useful for some task.

A simple arithmetic task:
A question answering task:

- Utterance: *Where was Obama born?*
- Logical form: `(place_of_birth barack_obama)`
- Denotation: `Honolulu`

A virtual travel agent task:

- Utterance: *Show me flights to Montreal leaving tomorrow.*
- Logical form: `(and (type flight) (destination montreal) (departure_date 2014.12.09))`
- Denotation: `(list ...)`

By parsing utterances into logical forms, we obtain a rich representation that
enables much deeper, context-aware understanding beyond the words.  With the
rise of natural language interfaces, semantic parsers are becoming increasingly
more powerful and useful.





### Logical  reasoning operations:
#### [Investigating Table-to-Text Generation Capabilities of LLMs in Real-World Information Seeking Scenarios]:
"To address this issue, application developers could tailor the table-to-text generation systems to generate multiple insights that encompass **different logical reasoning operations (Perlitz et al., 2022; Zhao et al., 2023b).**"

#### [Diversity Enhanced Table-to-Text Generation via Logic-Type Control]: 

https://arxiv.org/pdf/2205.10938.pdf

#### [Proceedings of the 17th Conference of the European Chapter of the Association for Computational Linguistics, pages 554–561
May 2-6, 2023 ©2023 Association for Computational LinguisticsLOFT: Enhancing Faithfulness and Diversity for Table-to-Text
Generation via Logic Form Control]:

https://aclanthology.org/2023.eacl-main.40.pdf<br/>
https://github.com/Yale-LILY/LoFT

