# Annotation automatique
Voici mon projet d'annotation automatique pour le cours d'enrichissement de corpus.

# Pour commencer
Pour éviter les conflits de version, nous allons créer un environnement virtuel.

Pour créer un environnement virtuel, vous pouvez procéder comme cela : 

`python3 -m venv nom_du_venv`
`source nom_du_venv/bin/activate`


La deuxième commande permet d’activer l’environnement. Lorsque c’est fait, vous verrez entre parenthèse le nom de votre environnement tout à gauche de la ligne de commande.

`pip install -r requirements.txt`


N’oubliez pas de désactiver l’environnement lorsque vous avez terminé.

`deactivate`


Ensuite, il va vous falloir télécharger les corpus. Pour cela, entrez cette commande dans le terminal :

`python3 -m spacy download fr_core_news_sm` 

