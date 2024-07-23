import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd

# Download the stopwords
nltk.download('stopwords')

# Get French stop words
french_stop_words = stopwords.words('french')

# Define the content of the files
qas_text = """Question: many volumes souples 1988 2016 volumes cartonnés 1955 à 1987 string contains jean 
Answers:
2

Question: many volumes souples 1988 2016 volumes cartonnés 1955 à 1987 string starts joseph 
Answers:
1"""

section_text = """les titres originaux américains de la série alice trahissent souvent lintrigue principale du roman contrairement aux titres français qui entretiennent davantage le mystère ainsi alice et le pickpocket ne dévoile rien tandis que le titre original clue jewel box en français lindice dans la boîte à bijoux donne à lavance l emplacement du trésor que recherchent les personnages il existe cependant des exceptions à cette règle alice et les fauxmonnayeurs indique clairement ce dont il sera question dans le roman tandis que son titre américain secret red gate farm littéralement le secret de la ferme le portail rouge est énigmatique il arrive que le titre français soit sans rapport avec la trame de l histoire dans alice et lombre chinoise la présence dune ombre chinoise nest quanecdotique et le corsaire dans alice et le corsaire est une simple référence à un navire qui aurait été volé par un corsaire du xixe siècle un dernier exemple alice et les chats persans où les petits félins ne prennent aucune part à lhistoire"""

# Create the TF-IDF vectorizer with French stop words
vectorizer = TfidfVectorizer(stop_words=french_stop_words)
tfidf_matrix = vectorizer.fit_transform([qas_text, section_text])

# Get feature names
feature_names = vectorizer.get_feature_names_out()

# Convert to dense format and inspect
dense_matrix = tfidf_matrix.todense()
qas_vector = dense_matrix[0].tolist()[0]
section_vector = dense_matrix[1].tolist()[0]

# Create DataFrame for better visualization
df = pd.DataFrame([qas_vector, section_vector], columns=feature_names, index=['qas_29_table_5', 'section_14'])

# Display the DataFrame
print(df)
