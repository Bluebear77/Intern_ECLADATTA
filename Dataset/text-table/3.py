import re

def remove_wiki_markup_corrected(text):
    # Remove text from '{{Voir homonymes|Roy}}' up to the first occurrence of "'''"
    text = re.sub(r'\{\{Voir homonymes\|.*?\}\}.*?(?=\n*\'{3})', '', text, flags=re.DOTALL)

    # Remove infoboxes
    text = re.sub(r'\{\{Infobox [^\}]*\}\}', '', text, flags=re.DOTALL)
    
    # Remove specific wiki markup patterns
    text = re.sub(r'\{\{[^\}]+\}\}', '', text)  # Matches other templates like {{Autre4}}
    text = re.sub(r'<\/?small>', '', text)  # Matches </small> and <small>
    text = re.sub(r'<br\s*\/?>', ' ', text)  # Matches <br> or <br />
    text = re.sub(r'<ref[^>]*>.*?<\/ref>', '', text, flags=re.DOTALL)  # Matches <ref group=*>*</ref>

    return text

# The input text:
text = """
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
 | adresse             = River City,
 | famille             = James Roy <small>(père)</small><br>Cécile Roy <small>(tante)</small>
 | affiliation         = 
 | entourage           = Sarah Berny <small>(gouvernante)</small><br>Bess Taylor <small>(amie)</small><br>Marion Webb <small>(amie)</small><br>Ned Nickerson <small>(ami)</small><br>Daniel Evans <small>(ami)</small><br>Bob Eddleton <small>(ami)</small><br>Togo <small>(chien)</small>
 | ennemi              = 
 | membre              = 
 | créateur            = [[Caroline Quine]]
 | interprète          = [[Bonita Granville]] <small>(1938-1939)</small><br>[[Pamela Sue Martin]] <small>(1977-1978)</small><br>Tracy Ryan <small>(1995)</small><br />[[Maggie Lawson]] <small>(2002)</small><br>[[Emma Roberts]] <small>(2007)</small><br>[[Sophia Lillis]] <small>(2019)</small><br>Kennedy McMann <small>(2019-...)</small>
 | film                = [[Nancy Drew... Detective]] (1938) [[Nancy Drew... Reporter]] (1939) [[Nancy Drew... Trouble Shooter]] (1939) [[Nancy Drew et l'escalier secret]] (1939) [[Nancy Drew, journaliste-détective]] (2002) [[Nancy Drew (film)|Nancy Drew]] (2007) [[Nancy Drew and the Hidden Staircase (film, 2019)|Nancy Drew and the Hidden Staircase]] (2019) 
 | roman               = 
 | pièce               = 
 | série               = [[The Hardy Boys/Nancy Drew Mysteries]] (1977-1979) Alice et les Hardy Boys (1995) [[Nancy Drew (série télévisée)|Nancy Drew]] (2019-...) 
 | album               = 
 | première apparition = [[1930 en littérature|1930]] (États-Unis)  [[1955 en littérature|1955]] (France)
 | dernière apparition = 
 | saison              = 
 | épisode             = 
 | éditeur             = [[Grosset & Dunlap]] puis [[Simon & Schuster]] (États-Unis) [[Hachette Jeunesse|Hachette]] (France)
}}

'''Alice Roy''' ('''Nancy Drew''' en version originale anglophone) est l’héroïne fictive d'une série américaine de [[roman (littérature)|romans]] policiers pour la jeunesse signée du [[Pseudonyme|nom de plume]] collectif [[Caroline Quine]], et publiée aux États-Unis à partir de 1930 par [[Grosset & Dunlap]]. 

En France, la série est parue pour la première fois en [[1955 en littérature|1955]] aux éditions [[Hachette Jeunesse|Hachette]] dans la collection [[Bibliothèque verte]] jusqu'en 2011. 

Très grand succès de librairie, dix millions d’exemplaires ont été vendus en France de 1955 à 1974 chez [[Hachette Jeunesse|Hachette]]<ref>Raymond Perrin , Histoire du polar jeunesse : Romans et bandes dessinées, L'Harmattan, 2011, page 36.</ref>.

Depuis 2011, la série paraît dans la collection [[Bibliothèque rose]] (catégorie Classiques de la Rose). Elle a également été partiellement éditée dans les collections [[Idéal-Bibliothèque]] (1964 à 1981), [[La Galaxie (collection)|La Galaxie]] (1971 à 1978) et « Masque jeunesse » (1983 à 1985) des éditions Hachette.
"""

# Apply the function
corrected_cleaned_text = remove_wiki_markup_corrected(text)
print(corrected_cleaned_text.strip())
