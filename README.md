# Projet python pour la datascience

# Titre

Problématique : Dans quelle mesure le niveau socio-économique détermine-t-il l'exposition aux maladies chroniques en France, et quelles pathologies présentent le gradient social le plus marqué ?

Résumé court à écrire

## 1. Comment lancer notre code ?

1. **Lancer VSCode** (un service Onyxia ou ouvrir VSCode).
2. Allez dans l'onglet **Fichiers**.
3. **Clic droit** dans votre espace de travail.
4. Sélectionnez **Télécharger**.
5. Choisissez le fichier `.zip`.
6. Assurez-vous que vous vous trouvez dans le dossier où vous avez téléchargé le fichier `.zip`.
7. Ouvrez un terminal et exécutez le code suivant en remplaçant `nom_fichier` par le nom du fichier `.zip` :

```bash
unzip <nom_fichier>.zip
```

8. Ouvrez maintenant le dossier.
9. Ouvrir le notebook main.ipynb et cliquer sur Run All.

## 2. Nos données

### 2.1 Jeu de données utilisés

Ce projet mobilise deux sources de données complémentaires :

- **Les données Drees (ER 1243)** : taux de prévalence et d'incidence de maladies chroniques ventilés par variables socio-démographiques, disponibles sur data.gouv.fr
- **Les données Insee (Filosofi)** : indicateurs socio-économiques par région (taux de pauvreté, revenu médian), également disponibles sur data.gouv.fr

Les deux sources sont chargées directement via l'API de data.gouv.fr, ce qui garantit la reproductibilité du projet.

Voici les liens des pages où nous avons trouvé ces données : 
- **Inégalités sociales face aux maladies chroniques (ER 1243) :** https://www.data.gouv.fr/datasets/inegalites-sociales-face-aux-maladies-chroniques-er-1243
- **Filosofi :** https://www.data.gouv.fr/datasets/carroyage-filosofi-revenus-pauvrete-et-niveau-de-vie-en-2019-1

### 2.2 Variables d'intérêt

Voici une liste de nos variables d'intérêts : 
- **Dd**

## 3. Statistiques descriptives et visualisation 

Présenter les statisques descriptives et visualisations 

## 4. Modélisation : choix du modèle et des variables

### 4.1 Clustering des pathologies selon leur profil d'inégalité sociale

L'objectif de ce clustering est de regrouper les maladies chroniques selon la forme de leur gradient social et ainsi regarder si certaines touchent les populations les plus modestes, les plus aisées ou bien n'ont pas de gradient social marqué.

Pour cela, les variables d'intérêts vont être : 
- **varTauxLib (Dress):** Identifiant de la maladie, par 

| Variable | Source | Rôle | Valeurs possibles |
|---|---|---|---|
| `varTauxLib` | DREES | Identifiant de la maladie (index de la matrice) | Ex. "Diabète", "Maladies cardiovasculaires"... |
| `valGroupage` | DREES | Décile de revenu (colonnes de la matrice) | 1 (plus modeste) à 10 (plus aisé) |
| `txStandDir` | DREES | Taux de prévalence standardisé direct (valeur de la matrice) | Taux entre 0 et 1 |

**Filtres appliqués :**
- `varGroupage == 'FISC_NIVVIEM_E2015_S_moy_10'` : on ne garde que la ventilation 
  par décile de revenu
- `type == 'prevalence'` : on travaille sur la prévalence uniquement
- `varPartition` est vide : on prend la vue nationale, sans partition régionale ou par sexe

**Pourquoi ces variables ?**  
L'objectif du clustering est de caractériser la *forme* du gradient social de chaque 
maladie. Le décile de revenu est la variable la plus directe pour cela : en construisant 
un profil décile 1 → décile 10 pour chaque maladie, on capture si la maladie touche 
plutôt les plus modestes, les plus aisés, ou de manière uniforme.

**Remarque sur la standardisation des taux :**  
On utilise `txStandDir` (taux standardisé par la méthode directe) plutôt que 
`txNonStand` afin de s'affranchir des effets de structure d'âge et de sexe 
entre les groupes — ce qui permet une comparaison plus juste entre déciles.

### 4.2 Regression : déterminants socio-économiques du taux de prévalance

## 5. Structure de notre dépôt

**Fichier principal :** Notre ficher principal est le Jupyter Notebook intitulé main.ipynb.

**Fichier d'installation des packages nécessaires :** Le fichier requirements.txt contient tous les packages nécessaires au projet et qu'il faudra installer (la cellule pour les installer est présente dans le notebook).

**Fichier avec les fonctions annexes :** Le fihcier fonctions.py contient toutes les fonctions annexes nécessaires au projet qui sont importées dans le notebook.