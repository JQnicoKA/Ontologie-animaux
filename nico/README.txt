Lancer le programme peut être fait en deux étapes:
1. Installer les requirements avec la commande "pip install -r requirements.txt"
2. Lancer le fichier gui.py et suivre les indications, les modèles ML utilisés seront ceux que nous avons déjà généré

Pour créer vous même les modèles, il vous faut d'abord récupérer les images depuis Kaggle,
Ceci peut être réalisé en ruinant les commandes dans le fichier commande.txt

Une démonstration vidéo du projet est également accessible :
Demonstration.mkv

Le rapport du projet :
Rapport_DS51.docx

Vous pouvez trouver ici les rôles de tous les fichiers présents dans le projet :

Génération de l'ontologie OWL :
Ontologie.ipynb

Dossier requirements à installer :
Requirements.txt

Stockage des images :
Dans le dossier "images", les images sont classées en données train, test et valid

Génération des modèles de Machine learning : 
Dans le dossier construct_model, un fichier pour la génération de chaque modèle

Modèles exportés : 
Le code de génération du modèle pour classifier Mammifère / Poisson / Oiseau : Google_superclass.pt
Le code de génération du modèle pour classifier Requin / Poisson rouge : Google_poissons.pt
Le code de génération du modèle pour classifier Aigle / Passerin indigo : Google_oiseaux.pt
Le code de génération du modèle pour classifier Loup / Ours : Google_mammiferes.pt

Interface utilisant les modèles exportés :
Gui.py
