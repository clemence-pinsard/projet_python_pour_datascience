# Projet python pour la datascience

# Titre

Problématique : Dans quelle mesure le niveau socio-économique détermine-t-il l'exposition aux maladies chroniques en France, et quelles pathologies présentent le gradient social le plus marqué ?

Résumé court à écrire

## 1. Comment lancer notre code ?

Lancer VSCode (un service Onyxia ou ouvrir VSCode).

Allez dans l'onglet « Fichiers ».
Cliquez avec le bouton droit de la souris dans votre espace de travail.
Sélectionnez « Télécharger ».
Choisissez le fichier .zip.
Assurez-vous que vous vous trouvez dans le dossier où vous avez téléchargé le fichier .zip.
Ouvrez un terminal et exécutez le code suivant en remplaçant « nom_fichier » par le nom du fichier .zip :
unzip <nom_fichier>.zip
Ouvrez maintenant le dossier.

Ouvrir le notebook main.ipynb et cliquer sur Run All.

## 2. Nos données

### 2.1 Jeu de données utilisés

Ce projet mobilise deux sources de données complémentaires :

- **Les données Drees (ER 1243)** : taux de prévalence et d'incidence de maladies chroniques ventilés par variables socio-démographiques, disponibles sur data.gouv.fr
- **Les données Insee (Filosofi)** : indicateurs socio-économiques par région (taux de pauvreté, revenu médian), également disponibles sur data.gouv.fr

Les deux sources sont chargées directement via l'API de data.gouv.fr, ce qui garantit la reproductibilité du projet.

Inégalités sociales face aux maladies chroniques (ER 1243) 
https://www.data.gouv.fr/datasets/inegalites-sociales-face-aux-maladies-chroniques-er-1243

Filosofi
https://www.data.gouv.fr/datasets/carroyage-filosofi-revenus-pauvrete-et-niveau-de-vie-en-2019-1

### 2.2 Variables d'intérêt

Lister et présenter les variables d'intérêts (avec une courte explication)

## 3. Statistiques descriptives et visualisation 

Présenter les statisques descriptives et visualisations 

## 4. Modélisation : choix du modèle et des variables

### 4.1 Clustering des pathologies selon leur profil d'inégalité sociale

### 4.2 Regression : déterminants socio-économiques du taux de prévalance

## 5. Structure de notre dépôt

**Fichier principal :** Notre ficher principal est le Jupyter Notebook intitulé main.ipynb.

**Fichier d'installation des packages nécessaires :** Le fichier requirements.txt contient tous les packages nécessaires au projet et qu'il faudra installer (la cellule pour les installer est présente dans le notebook).

**Fichier avec les fonctions annexes :** Le fihcier fonctions.py contient toutes les fonctions annexes nécessaires au projet qui sont importées dans le notebook.