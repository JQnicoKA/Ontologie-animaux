import requests

# Cette fonction détermine si notre entité est une sous-classe de la classe "animal"
def is_subclass_of_animal(entity_id):
    # URL de l'API Wikidata pour récupérer les informations sur une classe
    url = 'https://www.wikidata.org/w/api.php'

    # Paramètres de la requête
    params = {
        'action': 'wbgetentities',
        'format': 'json',
        'ids': entity_id,
        'props': 'claims',
    }

    try:
        # Envoi de la requête à l'API
        response = requests.get(url, params=params)
        response.raise_for_status()

        # Analyse de la réponse JSON
        data = response.json()

        # Récupération de la classe parente
        if 'P279' in data['entities'][entity_id]['claims']:
            subclass_of_claims = data['entities'][entity_id]['claims']['P279']
            for claim in subclass_of_claims:
                if 'mainsnak' in claim and 'datavalue' in claim['mainsnak']:
                    datavalue = claim['mainsnak']['datavalue']
                    if 'value' in datavalue and 'id' in datavalue['value']:
                        parent_class_id = datavalue['value']['id']
                        if parent_class_id == 'Q729':
                            return True
                        else:
                            if is_subclass_of_animal(parent_class_id):
                                return True
                            else:
                                return False
        return False

    except requests.exceptions.RequestException as e:
        print('Une erreur s\'est produite lors de la requête :', e)

# Cette fonction détermine si notre entité est une sous-catégorie de la classe "animal" dans le taxon
def is_subtaxon_of_animal(entity_id):
    # URL de l'API Wikidata pour récupérer les informations sur une classe
    url = 'https://www.wikidata.org/w/api.php'

    # Paramètres de la requête
    params = {
        'action': 'wbgetentities',
        'format': 'json',
        'ids': entity_id,
        'props': 'claims',
    }

    try:
        # Envoi de la requête à l'API
        response = requests.get(url, params=params)
        response.raise_for_status()

        # Analyse de la réponse JSON
        data = response.json()

        # Récupération de la classe parente
        if 'P171' in data['entities'][entity_id]['claims']:
            subtaxon_of_claims = data['entities'][entity_id]['claims']['P171']
            for claim in subtaxon_of_claims:
                if 'mainsnak' in claim and 'datavalue' in claim['mainsnak']:
                    datavalue = claim['mainsnak']['datavalue']
                    if 'value' in datavalue and 'id' in datavalue['value']:
                        parent_taxon_id = datavalue['value']['id']
                        if parent_taxon_id == 'Q729':
                            return True
                        else:
                            if is_subtaxon_of_animal(parent_taxon_id):
                                return True
                            else:
                                return False
        return False

    except requests.exceptions.RequestException as e:
        print('Une erreur s\'est produite lors de la requête :', e)


# Cette fonction renvoie un tableau de data correpondant à chaque élément cohérent à notre recherche
def recherche_entity_wikidata(nom_animal):
    # URL de l'API Wikidata
    url = 'https://www.wikidata.org/w/api.php'

    # Paramètres de la requête
    params = {
        'action': 'wbsearchentities',
        'format': 'json',
        'language': 'en',
        'type': 'item',
        'search': nom_animal
    }

    try:
        # Envoi de la requête à l'API
        response = requests.get(url, params=params)
        response.raise_for_status()

        # Analyse de la réponse JSON
        data = response.json()

        return data['search']

    except requests.exceptions.RequestException as e:
        print('Une erreur s\'est produite lors de la requête :', e)


# Exemple d'utilisation
# nom_animal = 'Brambling'
# tab_ids = recherche_entity_wikidata(nom_animal)

# i=0
# for result in tab_ids:
#     entity_id = result.get('id')
#     print(entity_id)
#     if is_subtaxon_of_animal(entity_id):
#         i=1
#         print(f"{nom_animal} est associé à une instance d'animal sur Wikidata.")
#         break

# if i==0:
#     print(f"{nom_animal} n'est pas associé à une instance d'animal sur Wikidata.")





# Cette fonction construit un dictionnaire avec les différents labels inscrits dans le fichier LOC_synset_mapping.txt
def lire_fichier_texte(nom_fichier):
    dictionnaire_resultats = {}

    with open(nom_fichier, 'r') as fichier:
        lignes = fichier.readlines()

        for ligne in lignes:
            # Diviser la ligne en éléments séparés par une virgule
            elements = ligne.strip().split(',')

            # Récupérer les 9 premiers caractères comme valeur
            valeur = elements[0][:9]

            # Ajouter le premier élément comme clé avec la valeur associée
            dictionnaire_resultats[elements[0][10:].strip()] = valeur

            # Ajouter les éléments suivants comme clés avec la valeur associée
            for element in elements[1:]:
                dictionnaire_resultats[element.strip()] = valeur

    return dictionnaire_resultats


# Code
nom_fichier = 'LOC_synset_mapping.txt'
resultats = lire_fichier_texte(nom_fichier)
tab_to_download = []
for cle, valeur in resultats.items():

    tab_entities = recherche_entity_wikidata(cle)

    i=0
    for result in tab_entities:
        # Pour chaque resultat dans WikiData correspondant à notre recherche, on extrait l'ID
        entity_id = result.get('id')
        print(entity_id)
        if is_subtaxon_of_animal(entity_id):
            i=1
            print(f"{cle} est associé à une instance d'animal sur Wikidata.")
            tab_to_download.append(cle)
            break
        elif is_subclass_of_animal(entity_id):
            i=1
            print(f"{cle} est associé à une instance d'animal sur Wikidata.")
            tab_to_download.append(cle)
            break

    if i==0:
        print(f"{cle} n'est pas associé à une instance d'animal sur Wikidata.")


        
