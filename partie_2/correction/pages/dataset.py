""" Code du dashboard `dataset` qui affiche les données du corpus sous la forme d'une table filtrable et triable.

Il permet également d'afficher le document numérisé d'une édition en particulier
grâce à l'API IIIF de Gallica et au visualiseur Mirador.
"""

import dash
import pandas as pd

dash.register_page(__name__, path="/")
# Avec l'option path..., les URL "/"" et "/dataset" afficheront ce dashbaord dans un contexte multipages.


data = pd.read_csv("../presse_xix-xxe.csv", parse_dates=["date"]).sample(1000)

titres = data.titre.unique()

layout = dash.html.Div(
    [
        dash.html.H1("Explorer le corpus"),
        dash.dcc.Dropdown(options=titres, id="selecteur-titre"),
        dash.dash_table.DataTable(
            data=data.to_dict("records"),
            columns=[{"name": col, "id": col} for col in data.columns],
            sort_action="native",
            filter_action="native",
            id="table-corpus",
            style_table={
                "maxHeight": "400px",
                "overflowY": "scroll",
            },
            row_selectable="single",
        ),
        dash.html.Iframe(
            id="mirador",
            width="100%",
            height="800px",
        ),
    ]
)


@dash.callback(
    dash.dependencies.Output("table-corpus", "data"),
    [dash.dependencies.Input("selecteur-titre", "value")],
)
def filter_table_avec_titre(titre):
    if not titre:
        return data.to_dict("records")
    return data[data.titre == titre].to_dict("records")


@dash.callback(
    dash.Output("mirador", "src"),
    [dash.Input("table-corpus", "selected_rows")],
    [dash.Input("table-corpus", "data")],
)
def affiche_iiif_documents(idx_lignes_sélectionnées, table):

    if not idx_lignes_sélectionnées:
        return ""

    # Une seule ligne peut être sélectionnée grace à row_selectable="single"
    ligne = idx_lignes_sélectionnées[0]

    if ligne >= len(table):
        return ""

    ark = table[ligne]["ark"]
    gallica_iiif = f"https://gallica.bnf.fr/iiif/ark:/12148/{ark}/manifest.json"
    iframe_embed = f"https://projectmirador.org/embed/?iiif-content={gallica_iiif}"

    return iframe_embed


if __name__ == "__main__":
    # ⁉️ Qu'est-ce que c'est que ce IF étrange ?
    #       La variable spéciale  __name__ est une variable spéciale fournie automatiquement par Python.
    #       Si le fichier est importé, __name__ contient le nom du module importé (i.e. le nom du fichier sans le .py).
    #       Si le fichier est exécuté directement, __name__ contient la valeur "__main__".
    #
    #       Donc, cette condition se traduit ainsi :
    #       "Si le fichier est exécuté directement (avec `python ./dataset.py`), alors crée une application Dash et lance le serveur."
    #        Mais si on importe ce fichier dans un autre script, comme un module (avec `import dataset`), alors ne fait rien.
    #       L'intérêt est de pouvoir importer les fonctions et classes définies dans ce fichier sans forcément lancer le serveur.
    #       On se servira de ce mécanisme un peu plus tard.

    # 1. Instanciation
    app = dash.Dash()

    # 2. Layout : assignation du layout déclaré plus haut
    app.layout = layout

    # print(app.layout.to_plotly_json()) # Debug  à dé-commenter au besoin : affiche le layout en JSON

    # 3. Lancement du serveur
    app.run(debug=True)
