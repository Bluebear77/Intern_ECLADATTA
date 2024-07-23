# https://huggingface.co/sentence-transformers/paraphrase-multilingual-mpnet-base-v2

# pip install -U sentence-transformers


from sentence_transformers import SentenceTransformer
sentences = ["This is an example sentence", "Each sentence is converted"]

model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-mpnet-base-v2')
embeddings = model.encode(sentences)
print(embeddings)

