1.para.py: extract text from the instance_i.json.

2. clean.py:remove wikimarkup and clean text.

3. qs.py: extract qas from the synthetic_qa_output_instance_i_v6.json

4. embedding.py: create embeddings for: each paragraph of the wikipage & all the qas belongs to the same table.

5. cosine.py: calculate the cosine similarity between [ each text file in ./embedding/qas/qas_i , every text file in the ./embedding/text/instance_i].


6. report.py: generate report and plots for the similairty score.


*. jaccard.py: calculate the jaccard similarity between [ each text file in ./embedding/qas/qas_i , every text file in the ./embedding/text/instance_i]. 