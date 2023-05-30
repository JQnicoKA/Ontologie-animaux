import requests
import re

def search_animal_in_wikidata(animal_label):
    api_url = "https://www.wikidata.org/w/api.php"
    params = {
        "action": "wbsearchentities",
        "format": "rdf",
        "language": "en",
        "type": "item",
        "search": animal_label
    }
    response = requests.get(api_url, params=params)
    data = response.json()
    return data["search"]

file_path = "LOC_synset_mapping.txt"
with open(file_path, "r") as file:
    for line in file:
        match = re.match(r"n(\d+) (.*)", line)
        if match:
            image_id = match.group(1)
            image_content = match.group(2)
            # Effectuez la recherche dans Wikidata en utilisant le contenu de l'image
            results = search_animal_in_wikidata(image_content)
            if results:
                # La ligne correspond à un animal, faites quelque chose avec l'identifiant et le contenu
                print("Animal trouvé :")
                print("Identifiant de l'image :", image_id)
                print("Contenu de l'image :", image_content)