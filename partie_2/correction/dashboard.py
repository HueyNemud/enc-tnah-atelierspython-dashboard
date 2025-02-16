import dash
from dash import dcc, html, Dash
import dash_bootstrap_components as dbc


# Crée une application et active le mode pages pour créer un dashboard multi-pages
app = Dash(
    __name__,
    use_pages=True,  # Active le mode pages
    external_stylesheets=[
        dbc.themes.BOOTSTRAP
    ],  # Permet d'utiliser les éléments de Bootstrap pour créer des composants graphiques plus "jolis".
)

app.title = "Presse XIX-XXe siècles"

app.layout = html.Div(
    [
        # L'élément dcc.Location sert à gérer les différentes pages de l'application
        dcc.Location(id="url", refresh=False),
        # On crée une bare de navigation Bootstrap
        dbc.Navbar(
            # ... qui contient un container...
            dbc.Container(
                [
                    # Avec un titre général
                    dbc.NavbarBrand(
                        "Données historiques de la presse française, XIX-XXe siècles",
                        href="/",
                    ),
                    # Et des éléments de menu  qui pointent vers les différentes pages de l'application
                    dbc.Nav(
                        [
                            # Page 1 : le corpus.
                            dbc.NavLink("Le corpus", href="/", active="exact"),
                            # Page 2 : l'évolution des illustrations
                            dbc.NavLink(
                                "Illustrations", href="/illustrations", active="exact"
                            ),
                        ]
                    ),
                ]
            )
        ),
        html.Div(dash.page_container),
    ]
)


# Si ce fichier est exécuté directement avec `python dashboard.py`, alors on démarre le serveur
if __name__ == "__main__":
    app.run_server(debug=True)
