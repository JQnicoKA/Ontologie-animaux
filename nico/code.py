import requests

tab_of_hierarchy = []


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
                        tab_of_hierarchy.append(parent_class_id)
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
                        tab_of_hierarchy.append(parent_taxon_id)
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
# nom_fichier = 'LOC_synset_mapping.txt'
# resultats = lire_fichier_texte(nom_fichier)
# for cle, valeur in resultats.items():

#     tab_entities = recherche_entity_wikidata(cle)

#     i=0
#     for result in tab_entities:
#         # Pour chaque resultat dans WikiData correspondant à notre recherche, on extrait l'ID
#         entity_id = result.get('id')
#         print(entity_id)
#         if is_subtaxon_of_animal(entity_id):
#             i=1
#             print(f"{cle} est associé à une instance d'animal sur Wikidata")
#             with open("resume.txt", "a") as fichier:
#                 hierarchy = " ".join(str(valeur) for valeur in tab_of_hierarchy)
#                 fichier.write("(" + cle + ") " + entity_id + " " + valeur + " taxon " + hierarchy + "\n")
#             #On vide le tableau qui contient la hiérarchie
#             tab_of_hierarchy.clear()
#             break
#         elif is_subclass_of_animal(entity_id):
#             i=1
#             print(f"{cle} est associé à une instance d'animal sur Wikidata.")
#             with open("resume.txt", "a") as fichier:
#                 hierarchy = " ".join(str(valeur) for valeur in tab_of_hierarchy)
#                 fichier.write("(" + cle + ") " + entity_id + " " + valeur + " class " + hierarchy + "\n")
#             #On vide le tableau qui contient la hiérarchie
#             tab_of_hierarchy.clear()
#             break

#     if i==0:
#         print(f"{cle} n'est pas associé à une instance d'animal sur Wikidata.")



################################################
####RECHERCHE DES NOMS DE LA HIERARCHIE#########
################################################

# def get_entity_name(entity_id):
#     # Construction de l'URL de requête à l'API Wikidata
#     url = f"https://www.wikidata.org/w/api.php?action=wbgetentities&ids={entity_id}&format=json"

#     # Envoi de la requête à l'API Wikidata
#     response = requests.get(url)
#     data = response.json()

#     # Récupération du nom de l'entité
#     try:
#         entity_name = data["entities"][entity_id]["labels"]["en"]["value"]
#         return entity_name
#     except KeyError:
#         return None

# def get_unique_words_after_taxon(file_path):
#     unique_words = set()
#     with open(file_path, 'r') as file:
#         for line in file:
#             words = line.strip().split()
#             if 'taxon' in words:
#                 taxon_index = words.index('taxon')
#                 for word in words[taxon_index + 1:]:
#                     if word not in unique_words:
#                         unique_words.add(word)
#     return list(unique_words)

# maliste = get_unique_words_after_taxon("resume.txt")

# i =0
# for entity_id in maliste:

#     entity_name = get_entity_name(entity_id)
#     if entity_name:
#         with open("hierarchy.txt", "a") as fichier:
#             hierarchy = " ".join(str(valeur) for valeur in tab_of_hierarchy)
#             fichier.write(entity_name + " " + entity_id + "\n")
#         i +=1
#         print(i)
#     else:
#         print(f"L'entité {entity_id} n'a pas été trouvée.")


################################################
####FILTRER LES LIGNES DE MOINS DE 30  #########
################################################

# # Ouvrir le fichier d'entrée en lecture
# with open('resume.txt', 'r') as file:
#     # Lire toutes les lignes du fichier
#     lines = file.readlines()

# # Créer une liste pour stocker les lignes à conserver
# processed_lines = []

# # Parcourir chaque ligne du fichier
# for line in lines:
#     # Séparer la ligne en entités
#     entities = line.strip().split(' ')

#     # Vérifier si la ligne contient moins ou égal à 4 entités
#     if len(entities) <= 30:
#         # Ajouter la ligne à la liste des lignes à conserver
#         processed_lines.append(line)

# # Ouvrir le fichier de sortie en écriture
# with open('resume_filtre_30.txt', 'w') as file:
#     # Écrire les lignes à conserver dans le fichier de sortie
#     for line in processed_lines:
#         file.write(line)

# print("Lignes traitées ont été écrites dans le nouveau_fichier.txt.")


#######################################################
#### SUPPRIMER LES LIGNES QUI ONT LE MEME ID  #########
#######################################################

# fichier_entree = open("resume_filtre_30.txt", "r")
# fichier_sortie = open("resume_filtre_30_nodoublons.txt", "w")

# identifiants_deja_rencontres = set()

# for ligne in fichier_entree:
#     fermeture_parenthese_index = ligne.find(")")
#     if fermeture_parenthese_index != -1:
#         texte_apres_parenthese = ligne[fermeture_parenthese_index + 1:].strip()
#         mots_apres_parenthese = texte_apres_parenthese.split()
#         if len(mots_apres_parenthese) > 0:
#             identifiant = mots_apres_parenthese[0] # Le premier "mot" après la parenthèse ")"
#             if identifiant not in identifiants_deja_rencontres: # Si l'identifiant est unique
#                 fichier_sortie.write(ligne)  # Écriture de la ligne dans le fichier de sortie
#                 identifiants_deja_rencontres.add(identifiant)

# fichier_entree.close()
# fichier_sortie.close()




########################################################################
####AUTOMATISATION DU CODE RDF POUR LA DÉFINITION DES VARIABLES#########
########################################################################

# import re

# entites = []
# identifiants = []

# with open('resume_filtre_30_nodoublons.txt', 'r') as file: # Ouverture du fichier contenant les animaux et leur hiérarchie
#     for ligne in file:
#         ouverture_parentheses_index = ligne.find("(")
#         fermeture_parenthese_index = ligne.find(")")
#         if ouverture_parentheses_index != -1 and fermeture_parenthese_index != -1:
#             texte_entre_parenthese = ligne[ouverture_parentheses_index +1 : fermeture_parenthese_index] # Le texte entre parentheses -> Le nom de l'animal
#             entites.append(texte_entre_parenthese) # On récupère le nom de l'animal
#         if fermeture_parenthese_index != -1:
#             texte_apres_parenthese = ligne[fermeture_parenthese_index + 1:].strip()
#             mots_apres_parenthese = texte_apres_parenthese.split()
#             if len(mots_apres_parenthese) > 0:
#                 identifiant = mots_apres_parenthese[0] # Le premier "mot" après la parenthèse ")" -> L'identifiant WikiData
#                 identifiants.append(identifiant) # On récupère l'identifiant WikiData de l'animal


# # Appliquer les filtres à chaque élément de la liste
# for i in range(len(entites)):
#     # Mettre en minuscule
#     entites[i] = entites[i].lower()
#     # Remplacer les espaces par des underscores
#     entites[i] = entites[i].replace(" ", "_")
#     # Remplacer les tirets par des underscores
#     entites[i] = entites[i].replace("-", "_")

# # Ecriture dans un fichier texte du code RDF de déclaration des variables
# for i in range(len(entites)):
#     with open("codeRDFLIB_variables.txt", "a") as fichier:
#         fichier.write(entites[i] + " = URIRef('https://www.wikidata.org/wiki/" + identifiants[i] + "')\n")



###########################################################################
####AUTOMATISATION DU CODE RDF POUR LA DÉFINITION DE LA HIERARCHIE#########
###########################################################################

# 1/ POUR g.add(( [animal], RDF.type, [type])) 
# import re

# entites = []
# identifiants = []

# with open('resume_filtre_30_nodoublons.txt', 'r') as file: # Ouverture du fichier contenant les animaux et leur hiérarchie
#     for ligne in file:
#         ouverture_parentheses_index = ligne.find("(")
#         fermeture_parenthese_index = ligne.find(")")
#         if ouverture_parentheses_index != -1 and fermeture_parenthese_index != -1:
#             texte_entre_parenthese = ligne[ouverture_parentheses_index +1 : fermeture_parenthese_index] # Le texte entre parentheses -> Le nom de l'animal
#             entites.append(texte_entre_parenthese) # On récupère le nom de l'animal
#         if fermeture_parenthese_index != -1:
#             texte_apres_parenthese = ligne[fermeture_parenthese_index + 1:].strip()
#             mots_apres_parenthese = texte_apres_parenthese.split()
#             if len(mots_apres_parenthese) > 0:
#                 identifiant = mots_apres_parenthese[0] # Le premier "mot" après la parenthèse ")" -> L'identifiant WikiData
#                 identifiants.append(identifiant) # On récupère l'identifiant WikiData de l'animal

# # Appliquer les filtres à chaque élément de la liste
# for i in range(len(entites)):
#     # Mettre en minuscule
#     entites[i] = entites[i].lower()
#     # Remplacer les espaces par des underscores
#     entites[i] = entites[i].replace(" ", "_")
#     # Remplacer les tirets par des underscores
#     entites[i] = entites[i].replace("-", "_")

# # Ecriture dans un fichier texte du code RDF de déclaration des variables
# for i in range(len(entites)):
#     with open("codeRDFLIB_hierarchie.txt", "a") as fichier:
#         fichier.write("g.add((" + entites[i] + ", RDF.type, '" + identifiants[i] + "'))\n")

# 2/ POUR g.add(( [type], RDF.type, [type]))  etc...

with open("resume_filtre_30_nodoublons.txt", 'r') as file:
    for line in file:
        words = line.strip().split()
        if 'taxon' in words:
            taxon_index = words.index('taxon')
            for i in range(len(words[taxon_index + 1:]) - 1):
                with open("codeRDFLIB_hierarchie_deuxieme.txt", "a") as fichier:
                    fichier.write("g.add((" + words[taxon_index + 1:][i] + ", RDF.type, '" + words[taxon_index + 1:][i+1] + "'))\n")
fichier.close()



################################################
####COMPTER LES LIGNES D'UN FICHIER    #########
################################################

# def compter_lignes(fichier):
#     with open(fichier, 'r') as f:
#         lignes = f.readlines()
#         nombre_lignes = len(lignes)
#     return nombre_lignes

# # Exemple d'utilisation
# fichier = 'resume_filtre_30_nodoublons.txt'
# nombre_lignes = compter_lignes(fichier)
# print("Nombre de lignes :", nombre_lignes)

