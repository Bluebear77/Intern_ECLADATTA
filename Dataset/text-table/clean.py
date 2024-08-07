import os
import glob
import re
import nltk
from nltk.corpus import stopwords

# Download necessary NLTK data
nltk.download('punkt')
nltk.download('stopwords')

def remove_wiki_markup(text):
    # Remove text between {{Voir homonymes| and ''' (including these patterns)
    text = re.sub(r'\{\{Voir homonymes\|.*?\'\'\'', '', text, flags=re.DOTALL)
    text = re.sub(r'\{\{Infobox[^}]*\}\}(?:(?!\{\{|\}\}).|\{\{[^}]*\}\})*\}\}', '', text, flags=re.DOTALL)

    # Remove infoboxes
    text = re.sub(r'\{\{Infobox [^\}]*\}\}', '', text, flags=re.DOTALL)
    
    # Remove specific wiki markup patterns
    text = re.sub(r'\{\{[^\}]+\}\}', '', text)  # Matches other templates like {{Autre4}}
    text = re.sub(r'<\/?small>', '', text)  # Matches </small> and <small>
    text = re.sub(r'<br\s*\/?>', ' ', text)  # Matches <br> or <br />
    text = re.sub(r'<ref[^>]*>.*?<\/ref>', '', text, flags=re.DOTALL)  # Matches <ref group=*>*</ref>
    
    # Print intermediate text for debugging
    # print("Intermediate text after removing markup:")
    # print(text)

    return text

def clean_text(dirty_text, language='french'):
    # Remove Wikipedia markup
    dirty_text = remove_wiki_markup(dirty_text)

    # Tokenize words
    words = nltk.word_tokenize(dirty_text, language)

    # Remove punctuation
    words = [re.sub(r'[^\w\s]', '', word) for word in words]
    
    # Convert to lowercase
    words = [word.lower() for word in words]

    # Remove stopwords
    stop_words = set(stopwords.words(language))
    words = [word for word in words if word not in stop_words]

    # Join words back into a string
    cleaned_text = ' '.join(words)

    # Return the cleaned text
    return cleaned_text

def process_text_file(file_path, output_dir):
    # Read the file content
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    # Clean the text
    cleaned_text = clean_text(text)

    # Determine the output path
    relative_path = os.path.relpath(file_path, './text/v1')
    output_path = os.path.join(output_dir, relative_path)

    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Write the cleaned text to the output file
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(cleaned_text)

    print(f"Processed and saved: {output_path}")

# Get the list of text files matching the pattern in the ./text/v1 directory
text_files = glob.glob('./text/v1/instance_*/section_*.txt')

# Process each text file
for text_file in text_files:
    process_text_file(text_file, './text/v2')

print("Processing complete.")
