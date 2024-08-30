import os
import json
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

    # Remove infoboxes
    text = re.sub(r'\{\{Infobox [^\}]*\}\}', '', text, flags=re.DOTALL)
    
    # Remove specific wiki markup patterns
    text = re.sub(r'\{\{[^\}]+\}\}', '', text)  # Matches other templates like {{Autre4}}
    text = re.sub(r'<\/?small>', '', text)  # Matches </small> and <small>
    text = re.sub(r'<br\s*\/?>', ' ', text)  # Matches <br> or <br />
    text = re.sub(r'<ref[^>]*>.*?<\/ref>', '', text, flags=re.DOTALL)  # Matches <ref group=*>*</ref>
    
    # Print intermediate text for debugging
    print("Intermediate text after removing markup:")
    print(text)

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

def process_json_file(file_path):
    # Get the base file name without extension
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    
    # Create a directory named after the base file name under ./text
    output_dir = os.path.join(os.getcwd(), 'text', base_name)
    os.makedirs(output_dir, exist_ok=True)
    
    # Read the JSON file
    with open(file_path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
    
    extraction_metadata = data["_source"]["extractionMetadata"]
    
    # Iterate over each extraction metadata object
    for metadata in extraction_metadata:
        texts = metadata.get("texts", [])
        
        # Iterate over each section in texts
        for idx, section in enumerate(texts):
            title = section.get('title', 'Untitled')
            value = section.get('value', '')
            
            # Clean the text value
            cleaned_value = clean_text(value)
            
            # Construct the content to be written
            content = f"Title: {title}Value:{cleaned_value}"
            
            # Define the output file path
            output_file_path = os.path.join(output_dir, f'section_{idx+1}.txt')
            
            # Write the content to the output file
            with open(output_file_path, 'w', encoding='utf-8') as output_file:
                output_file.write(content)

# Debugging example with the input data directly
input_data = """
{{Voir homonymes|Roy}}
{{Autre4|la série de romans et le personnage|l'adaptation cinématographique de 2007|Nancy Drew (film)}}
{{Infobox Personnage (fiction)
 | charte couleur      = Roman
 | nom                 = Alice Roy
 | œuvre               = la série de romans « Alice »
 | image               = 
 | légende             = 
 | nom original        = Nancy Drew
 | nom alias           = 
 | naissance           = 
 | origine             = {{États-Unis}}
 | décès               = 
 | sexe                = Féminin
 | espèce              = 
 | cheveux             = Blonds
 | yeux                = Bleus
 | activité            = Détective amateur
 | caractéristique     = Orpheline de mère
 | adresse             = River City
 | famille             = {{Liste simple|
* James Roy <small>(père)</small>
* Cécile Roy <small>(tante)</small>
}}
 | affiliation         = 
 | entourage           = {{Liste simple|
* Sarah Berny <small>(gouvernante)</small>
* Bess Taylor <small>(amie)</small>
* Marion Webb <small>(amie)</small>
* Ned Nickerson <small>(ami)</small>
* Daniel Evans <small>(ami)</small>
* Bob Eddleton <small>(ami)</small>
* Togo <small>(chien)</small>
}}
 | ennemi              = 
 | membre              = 
 | créateur            = [[Caroline Quine]]
 | interprète          = {{Liste simple|
* [[Bonita Granville]] <small>(1938-1939)</small>
* [[Pamela Sue Martin]] <small>(1977-1978)</small>
* Tracy Ryan <small>(1995)</small>
* [[Maggie Lawson]] <small>(2002)</small>
* [[Emma Roberts]] <small>(2007)</small>
* [[Sophia Lillis]] <small>(2019)</small>
* Kennedy McMann <small>(2019-...)</small>
}}
 | film                = {{Liste simple|
* ''[[Nancy Drew... Detective]]'' <small>(1938)</small>
* ''[[Nancy Drew... Reporter]]'' <small>(1939)</small>
* ''[[Nancy Drew... Trouble Shooter]]'' <small>(1939)</small>
* ''[[Nancy Drew and the Hidden Staircase (film, 1939)|Nancy Drew and the Hidden Staircase]]'' <small>(1939)</small>
* ''[[Nancy Drew, journaliste-détective]]'' <small>(2002)</small>
* ''[[Nancy Drew (film)|Nancy Drew]]'' <small>(2007)</small>
* ''[[Nancy Drew and the Hidden Staircase (film, 2019)|Nancy Drew and the Hidden Staircase]]'' <small>(2019)</small>
}}
 | roman               = 
 | pièce               = 
 | série               = {{Liste simple|
* ''[[The Hardy Boys/Nancy Drew Mysteries]]'' <small>(1977-1979)</small>
* ''Alice et les Hardy Boys'' <small>(1995)</small>
* ''[[Nancy Drew (série télévisée)|Nancy Drew]]'' <small>(2019-...)</small>
}}
 | album               = 
 | première apparition = {{Liste simple|
* [[1930 en littérature|1930]] <small>(États-Unis)</small>
* [[1955 en littérature|1955]] <small>(France)</small>
}}
 | dernière apparition = 
 | saison              = 
 | épisode             = 
 | éditeur             = {{Liste simple|
* [[Grosset & Dunlap]] puis [[Simon & Schuster]] <small>(États-Unis)</small>
* [[Hachette Jeunesse|Hachette]] <small>(France)</small>
}}
}}

'''Alice Roy''' ('''Nancy Drew''' en version originale anglophone) est l’héroïne fictive d'une série américaine de [[roman (littérature)|romans]] policiers pour la jeunesse signée du [[Pseudonyme|nom de plume]] collectif [[Caroline Quine]], et publiée aux États-Unis à partir de 1930 par [[Grosset & Dunlap]]. 
"""


# Perform cleaning on the input data
cleaned_output = clean_text(input_data)

# Output the result for debugging
print("\nCleaned output:")
print(cleaned_output)

# To process actual files, uncomment below lines:
# json_files = glob.glob('./fr-multilingual-mpnet-base-v2/5-sample/input-json/instance_*.json')

# Process each JSON file
# for json_file in json_files:
#     process_json_file(json_file)

# print("Processing complete.")
