""" Code du dashboard `dataset` qui affiche les données du corpus sous la forme d'une table filtrable et triable.

Il permet également d'afficher le document numérisé d'une édition en particulier
grâce à l'API IIIF de Gallica et au visualiseur Mirador.
"""

import dash
import pandas as pd

data = ...  # 🏗️ Compléter moi : chargez les données depuis le CSV.

layout = ...  # 🏗️ Compléter moi : définissez ici le layout du dashboard

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
