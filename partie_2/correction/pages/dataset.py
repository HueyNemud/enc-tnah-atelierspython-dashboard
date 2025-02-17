import dash
from dash import dcc, html, dash_table, callback, Dash
from dash.dependencies import Input, Output
import pandas as pd

dash.register_page(__name__, path="/")  # ✅ / et /dataset affichent la même page

# Sample DataFrame
data = pd.read_csv(
    "../presse_xix-xxe_meta_arks.csv",
    parse_dates=["date"],
).sort_values("date")


# On récupère les titres uniques pour les utiliser dans la checklist
titres = data["titre"].unique()

layout = html.Div(
    [
        html.H3("Explorer la table de données complète"),
        dcc.Dropdown(
            id="sélecteur-titre",
            options=[{"label": cat, "value": cat} for cat in titres],
            value=titres[0],
            clearable=False,
        ),
        # Composant DataTable pour afficher la table de données
        dash_table.DataTable(
            id="table-corpus",
            columns=[{"name": col, "id": col} for col in data.columns],
            style_table={
                "maxHeight": "400px",
                "overflowY": "scroll",
            },
            filter_action="native",  # Permet de filtrer les données
            sort_action="native",  # Permet de trier les données
            row_selectable="single",  # Permet de sélectionner une seule ligne
            selected_rows=[],  # Par défaut, aucune ligne n'est sélectionnée
        ),
        # Conteneur pour le visualiseur IIIF Mirador
        html.Div(
            id="conteneur-mirador",
            children=[
                html.Iframe(
                    id="mirador",
                    style={"width": "100%", "height": "800px"},
                    src="",  # On initialise l'iframe avec un contenu vide
                )
            ],
        ),
    ]
)


@callback(Output("table-corpus", "data"), [Input("sélecteur-titre", "value")])
def update_table(titre_sélectionné):
    table_filtrée = data[data["titre"] == titre_sélectionné]
    return table_filtrée.to_dict("records")


@callback(
    Output("mirador", "src"),
    [Input("table-corpus", "selected_rows")],
    [Input("table-corpus", "data")],
)
def update_mirador(idx_lignes_sélectionnées, table):

    if not idx_lignes_sélectionnées:
        return ""

    # Une seule ligne peut être sélectionnée grace à row_selectable="single"
    ligne = idx_lignes_sélectionnées[0]

    if ligne >= len(table):
        return ""

    ark = table[ligne]["ark"]

    # On construit l'URL du manifeste IIIF
    iiif_manifest = f"https://gallica.bnf.fr/iiif/ark:/12148/{ark}/manifest.json"

    url_miradorembed = f"https://projectmirador.org/embed/?iiif-content={iiif_manifest}"
    # ... et on l'injecte dans l'iframe qui affiche Mirador
    # Puis on retourne le code HTML de l'iframe qui sera injecté dans "conteneur-mirador"
    return url_miradorembed


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
