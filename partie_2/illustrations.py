""" Code du dashboard `illustrations` qui affiche le graphique de l'évolution du nombre d'illustrations dans la presse.
"""

import dash
import pandas as pd
import plotly.express as px


# On charge les données à partir du fichier CSV
# - On parse la colonne "date" en tant que dates
# - On groupe les données par "titre" et par année, en rééchantillonnant à l'année
# - On somme les valeurs pour chaque groupe
# - groupby() placera "titre" et "date" en index. On préfère les avoir comme colonnes pour simplifier la manipulation,
#       donc on appelle reset_index() pour réinitialiser l'index et remettre les colonnes "titre" et "date" comme colonnes normales.
data = ...  # 🏗️ Compléter moi : chargez les données depuis le CSV.

layout = dash.html.Div(
    [
        # Titre de la page
        dash.html.H3("Les images dans la presse, une histoire en graphiques"),
        # Sélecteur de titre de presse
        ...,  # 🏗️ Compléter moi  : ajoutez les composants Checklist et Graph
    ]
)

...  # 🏗️ Compléter moi  : ajouter la déclaration du callback.
def tracer_courbes(selection):
    """Mets à jour le graphique en fonction des titres de presse sélectionnés"""
    ...  # 🏗️ Compléter moi : ajouter le corps de la fonction


if __name__ == "__main__":
    # 1. Instanciation
    app = dash.Dash()

    # 2. Layout : assignation du layout déclaré plus haut
    app.layout = layout

    # print(app.layout.to_plotly_json()) # Debug  à dé-commenter au besoin : affiche le layout en JSON

    # 3. Lancement du serveur
    app.run(debug=True)
