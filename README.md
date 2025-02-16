# Master TNAH - Atelier "Python pour les données de la recherche en histoire" - Dashboards

Bienvenue sur le dépôt du matériel, code et instructions, pour  réaliser la seconde séquence de l'atelier "Python pour les données de la recherche en histoire" du master Technologies numériques appliquées à l'histoire à l'École Nationale des Chartes.

Cette première séquence est dédiée à la réalisation d'un **tableau de bord**  pour explorer visuellement un tableau de données de grande taille.

Elle est composée de deux parties :

1. Une introduction au corpus, aux bibliothèques Python Pandas et Plotly pour créer les éléments de base du tableau de bord.
2. Un tutoriel pour construire le tableau de bord avec Dash.

Les deux séances s'appuient sur des données historiques réelles : les extractions des **métadonnées quantitatives de la presse française aux XIX-XXe siècles**, [produites par la BnF](https://api.bnf.fr/fr/metadonnees-quantitatives-de-la-presse-ancienne-xixe-xxe-siecles) dans le projet de recherche [Europeana Newspaper](http://www.europeana-newspapers.eu/) et diffusées sous license ouverte sur le portail de données de la BnF : [https://api.bnf.fr/fr/metadonnees-quantitatives-de-la-presse-ancienne-xixe-xxe-siecles](https://api.bnf.fr/fr/metadonnees-quantitatives-de-la-presse-ancienne-xixe-xxe-siecles)
Dernière mise à jour : **Février 2025**.

## Mise en place 🏗️

1. Télécharger le dépôt avec Git

```bash
git clone git@github.com:HueyNemud/enc-m2tnah-atelierspython-recordlinkage.git
```

2. Vérifier que Python 3.10 ou supérieur est utilisé

```bash
python --version
```

3. Au besoin, créez un nouvel environnement virtuel Python

```bash
python -m venv ~/python_atelierstnah
source ~/python_atelierstnah/bin/activate
```
