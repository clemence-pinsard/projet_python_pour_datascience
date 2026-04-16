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

Ce projet mobilise deux sources de données complémentaires issues des **données Drees (ER 1243)**. On récupère dans un premier temps la table maladie_chronique qui contient des variables telles que le taux de prévalence et d'incidence de maladies chroniques ventilés par variables socio-démographiques. Ainsi que la table et libelles qui permet de décoder les codes des modalités présents dans les colonnes `valGroupage` et `valPartition`.

Ces données sont disponibles sur data.gouv.fr. Les données sont ensuite chargées directement via l'API de data.gouv.fr, ce qui garantit la reproductibilité du projet.

Voici le lien de la page où nous avons trouvé ces données : 
- **Inégalités sociales face aux maladies chroniques (ER 1243) :** https://www.data.gouv.fr/datasets/inegalites-sociales-face-aux-maladies-chroniques-er-1243

### 2.2 Variables d'intérêt

Voici une liste de nos variables d'intérêts : 
- **poids1 (maladies_chroniques) :** Nombre de personnes atteintes
- **poidsTot (maladies_chroniques) :** Population totale du groupe observé
- **txNonStand (maladies_chroniques) :** Taux brut observé
- **txStandDir (maladies_chroniques) :** taux standardisé par méthode directe, utilisé pour comparer les groupes indépendamment de leur âge
- **txStandDirModBB et txStandDirModBH (maladies_chroniques) :** Bornes de l'intervalle de confiance du taux standardisé
- **txStandIndir (et ses bornes BB/BH) (maladies_chroniques) :** Taux standardisé par la méthode indirecte

- **type (maladies_chroniques) :** indique s'il s'agit de données de prévalence (nombre de cas à l'instant T) ou d'incidence (nombre de cas sur une période)
- **varTaux (maladies_chroniques) :** Code technique de la pathologie (ex : TOP_CVIC_CHR)
- **varTauxLib (maladies chroniques) :** Libellé complet de la maladie (ex: "Insuffisance cardiaque chronique")
- **cat (maladies_chroniques) :** Code de la grande catégorie de maladies
- **catLib (maladies_chroniques) :** Nom de la grande catégorie de maladies
- **I_cat (maladies_chroniques) :** Indicateur binaire utilisé pour distinguer les catégories

- **varGroupage / valGroupage (maladies_chroniques) :** la variable de ventilation et sa modalité (ex : décile de revenu, CSP, diplôme...)
- **varPartition / valPartition (maladies_chroniques) :** : Type/code de la zone géographique

- **var (libelles) :** Nom de la variable codée (ex: EAR_DIPLR_S pour le diplôme)
- **moda (libelles) :** Code de la modalité
- **moda_lib (libelles) :** Libellé compréhensible

## 3. Statistiques descriptives et visualisation 

Présenter les statisques descriptives et visualisations 

## 4. Modélisation : choix du modèle et des variables

### 4.1 Clustering des pathologies selon leur profil d'inégalité sociale

L'objectif de ce clustering est de regrouper les maladies chroniques selon la forme de leur gradient social et ainsi regarder si certaines touchent les populations les plus modestes, les plus aisées ou bien n'ont pas de gradient social marqué.

Pour cela, les variables d'intérêts vont être : 
- **varTauxLib (maladies_chroniques):** Identifiant de la maladie dont les valeurs possibles peuvent être "Diabète", "Maladies cardiovasculaires" ... 
- **valGroupage (maladies_chroniques):** Décile de revenu dont les valeurs possibles 1 (plus modeste) jusqu'à 10 (plus aisé)
- **txStandDir (maladies_chroniques) :** Taux de prévalense standardisé direct dont les valeurs sont comprises entre 0 et 1

Nous allons appliqué des filtres : 
- `varGroupage == 'FISC_NIVVIEM_E2015_S_moy_10'` pour ne garder que la ventilation par décile de revenu
- `type == 'prevalence'` pour travailler uniquement sur la prévalence
- `varPartition` est vide pour ne garder que la vue nationale (ne pas travailler par région ou sexe)

**Pourquoi ces variables ?**  
L'objectif du clustering est de caractériser la *forme* du gradient social de chaque maladie. Le décile de revenu est la variable la plus directe pour cela : en construisant un profil décile 1 → décile 10 pour chaque maladie, on capture si la maladie touche plutôt les plus modestes, les plus aisés, ou de manière uniforme.
 
On utilise `txStandDir` (taux standardisé par la méthode directe) plutôt que `txNonStand` afin de s'affranchir des effets de structure d'âge et de sexe entre les groupes — ce qui permet une comparaison plus juste entre déciles.

### 4.2 Regression : déterminants socio-économiques du taux de prévalance

L'objectif est d'identifier quels facteurs socio-économiques (niveau de vie, diplôme, catégorie socioprofessionnelle) sont les plus associés au taux de prévalence des maladies chroniques.

Pour cela, nos variables d'intérêts vont être :
- **txStandDir (maladies_chroniques) :** Notre variable cible qui correspond au taux de prévalence standardisé
- **varGroupage (maladies_chroniques) :** Une de nos variables explicatives donc le code qui nous intéresse est `FISC_NIVVIEM_E2015_S_moy_10` (décile de niveau de vie)
- **varTauxLib_ (maladies_chroniques) :** Une autre de nos variables explicatives 

Nous allons appliqué des filtres :
- `varGroupage == 'FISC_NIVVIEM_E2015_S_moy_10'` pour ne garder que la ventilation par décile
- `type == 'prevalence'` pour travailler uniquement sur la prévalence
- `varPartition` est vide pour avoir une vue nationale sans sous-partition par sexe

**Interprétation attendue du coefficient `decile` :**  Un coefficient négatif confirmera que les maladies chroniques touchent davantage les personnes modestes. Sa valeur indique de combien le taux de prévalence varie en moyenne quand on passe d'un décile au suivant, toutes maladies égales par ailleurs.

## 5. Structure de notre dépôt

**Fichier principal :** Notre ficher principal est le Jupyter Notebook intitulé main.ipynb.

**Fichier d'installation des packages nécessaires :** Le fichier requirements.txt contient tous les packages nécessaires au projet et qu'il faudra installer (la cellule pour les installer est présente dans le notebook).

**Fichier avec les fonctions annexes :** Le fihcier fonctions.py contient toutes les fonctions annexes nécessaires au projet qui sont importées dans le notebook.