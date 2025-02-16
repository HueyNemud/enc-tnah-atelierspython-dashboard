import dash
from dash import dcc, html, callback
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Enregistre ce fichier auprès de Dash afin qu'il soit considéré comme une page
# dans un dashboard multi-pages.
# On enregistre la page sous le nom du fichier actuel (__name__ une variable spéciale en Python qui contient le nom du fichier actuel, sans extension).
# La page s'appellera donc "illustrations" et sera par défaut accessible à l'url `/illustrations`dans  le dashboard.
dash.register_page(__name__)


# On charge les données à partir du fichier CSV
# - On parse la colonne "date" en tant que dates
# - On groupe les données par "titre" et par année, en rééchantillonnant à l'année
# - On somme les valeurs pour chaque groupe
# - groupby() placera "titre" et "date" en index. On préfère les avoir comme colonnes pour simplifier la manipulation,
#       donc on appelle reset_index() pour réinitialiser l'index et remettre les colonnes "titre" et "date" comme colonnes normales.
data = (
    pd.read_csv("../presse_xix-xxe_meta_arks.csv", parse_dates=["date"])
    .groupby(["titre", pd.Grouper(key="date", freq="YE")])
    .sum()
    .reset_index()
)

# On récupère les titres uniques pour les utiliser dans la checklist
titres = data["titre"].unique()


# Définition de la structure de la page
# --------------------------------------------------------
#
#  TITRE H3 "Les images dans la presse"
#
#        ______Checklist "selecteur-titre"__ _________
#           [  ]  Le Gaulois
#           [  ] Le Matin
#           [  ] ...
#        ___________________________________________
#
#        ______Graph "graphe-illustrations"________
#        |                        ICI  VA LE GRAPHIQUE !          |
#        ___________________________________________

# L'élément principal est conteneur DIV qui contiendra tous les autres éléments de la page
layout = html.Div(
    [
        # Titre de la page
        html.H3("Les images dans la presse"),
        # Sélecteur de titre de presse
        dcc.Checklist(
            id="sélecteur-titre",
            options=[{"label": titre, "value": titre} for titre in titres],
            value=[],  # Aucun titre sélectionné par défaut
        ),
        # Notre graphique !
        dcc.Graph(id="graphe-illustrations"),
    ]
)


# --------------------------------------------------------
# Définitions de la logique des interactions  entre les éléments de la page


@callback(
    Output("graphe-illustrations", "figure"),  # En sortie : on met à jour le graphique
    [
        Input("sélecteur-titre", "value")
    ],  # En entrée : on écoute les changements de sélection dans la checklist
)
def update_graph(titres_sélectionnés):
    """Met à jour le graphique en fonction des titres de presse sélectionnés"""

    fig = px.line()  # On crée un graphique vide qu'on remplira ensuite

    # On crée la courbe de l'évolution du nombre d'illustrations pour chaque titre sélectionné
    # Puis on ajoute chaque courbe au graphique
    for titre in titres_sélectionnés:
        df = data[data["titre"] == titre]
        fig.add_scatter(
            x=df["date"],
            y=df["nb_illustrations"],
            mode="lines",
            name=titre,
            line_shape="spline",
        )

    # Ajout de la légende et des titres des axes du graphique complet
    fig.update_layout(
        title="Illustrations par année",
        xaxis_title="Année",
        yaxis_title="Nombre d'illustrations",
    )

    # Finalement, on retourne le graphique créé : Dash se chargera de l'afficher à l'écran !
    return fig


# --------------------------------------------------------
# Si ce fichier est exécuté directement, on lance l'application Dash
# Attention : dans ce cas il faut commenter la ligne dash.register_page(__name__)
if __name__ == "__main__":
    # On crée une application Dash
    app = dash.Dash(__name__)

    # On définit la structure de la page à afficher
    app.layout = layout

    # On lance l'application en mode debug
    app.run_server(debug=True)
