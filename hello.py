import requests

def recherche_animal_wikidata(nom_animal):
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

        # Vérification si des résultats ont été trouvés
        for result in data['search']:
            if 'animal' in result.get('description', '').lower():
                return True

        return False
    except requests.exceptions.RequestException as e:
        print('Une erreur s\'est produite lors de la requête :', e)

# Exemple d'utilisation
# nom_animal = 'tiger'
# if recherche_animal_wikidata(nom_animal):
#     print(f"{nom_animal} est associé à une instance d'animal sur Wikidata.")
# else:
#     print(f"{nom_animal} n'est pas associé à une instance d'animal sur Wikidata.")


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
for cle, valeur in resultats.items():
    print(f"{cle} : {valeur}")

    if recherche_animal_wikidata(cle):
        print(f"{cle} OUIIIIIIII")
    else:
        print(f"{cle} NONNNNNNN")

