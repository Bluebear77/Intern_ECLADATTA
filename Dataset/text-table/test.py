from sentence_transformers import SentenceTransformer

# Read sentences from the file
with open('test.txt', 'r') as file:
    sentences = file.readlines()

# Strip newline characters from each sentence
sentences = [sentence.strip() for sentence in sentences]

# Load the model
model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-mpnet-base-v2')

# Encode the sentences
embeddings = model.encode(sentences)

# Print the embeddings
print(embeddings)
# Print the shape of the embeddings
print("Shape of the embeddings:", embeddings.shape)