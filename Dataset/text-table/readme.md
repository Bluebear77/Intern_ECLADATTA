para.py: extract text from the instance_i.json.

qs.py: extract qas from the synthetic_qa_output_instance_i_v6.json

embedding.py: create embeddings for: each paragraph of the wikipage & all the qas belongs to the same table.

cosine.py: calculate the cosine similarity between [ each text file in ./embedding/qas/qas_i , every text file in the ./embedding/text/instance_i]