""" Code du dashboard `illustrations` qui affiche le graphique de l'évolution du nombre d'illustrations dans la presse.
"""

import dash
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
    pd.read_csv("../presse_xix-xxe.csv", parse_dates=["date"])
    .groupby(["titre", pd.Grouper(key="date", freq="YE")])
    .sum()
    .reset_index()
)


layout = dash.html.Div(
    [
        # Titre de la page
        dash.html.H3("Les images dans la presse, une histoire en graphiques"),
        # Sélecteur de titre de presse
        dash.dcc.Checklist(
            id="selecteur-titre",
            options=data.titre.unique(),
            value=[],  # Aucun titre sélectionné par défaut
        ),
        dash.dcc.Graph(id="graphe-illustrations"),
    ]
)


# En sortie : on met à jour le graphique
# En entrée : on écoute les changements de sélection dans la checklist
@dash.callback(
    dash.Output("graphe-illustrations", "figure"),
    [dash.Input("selecteur-titre", "value")],
)
def tracer_courbes(selection):
    """Mets à jour le graphique en fonction des titres de presse sélectionnés"""

    fig = px.line()  # On crée un graphique vide qu'on remplira ensuite

    # On crée la courbe de l'évolution du nombre d'illustrations pour chaque titre sélectionné
    # Puis on ajoute chaque courbe au graphique
    for titre in selection:
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


if __name__ == "__main__":
    # 1. Instanciation
    app = dash.Dash()

    # 2. Layout : assignation du layout déclaré plus haut
    app.layout = layout

    # print(app.layout.to_plotly_json()) # Debug  à dé-commenter au besoin : affiche le layout en JSON

    # 3. Lancement du serveur
    app.run(debug=True)
