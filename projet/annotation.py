import spacy
from sklearn.metrics import precision_score, recall_score, f1_score
from bs4 import BeautifulSoup as bs

# Je fais le traitement avec spaCy
with open("texte_norme.txt") as fichier_corpus:
    nlp = spacy.load("fr_core_news_sm")
    corpus = fichier_corpus.read()
    doc = nlp(corpus)
    nb_words = list(corpus.split())
    corpus_count = len(nb_words)

# Contenu des colonnes
lignes = []
for token in doc:
    ligne_token = token.text
    ligne_lemme = token.lemma_
    ligne_pos = token.pos_
    ligne_dep = token.dep_
    lignes.append([ligne_token, ligne_lemme, ligne_pos, ligne_dep])

# Là je modifie la balise head pour mettre des modifications CSS notamment
code_html= """
<html>
<head>
    <meta charset="UTF-8">
    <title>Annotation automatique : résultats</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bulma@0.9.3/css/bulmaswatch.min.css">
    <link rel="stylesheet" href="https://unpkg.com/bulmaswatch/pulse/bulmaswatch.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/bulma/0.9.3/css/bulmaswatch.min.css">
    <script defer src="https://use.fontawesome.com/releases/v5.0.10/js/all.js"></script>
    <script src="https://code.jquery.com/jquery-3.5.1.min.js"></script>
    <script src="index.js"></script>
</head>
<body>
    <div>
        <label for="pages">Choisir un module : </label>
        <select id="pages" onchange="changePage(this.value)">
            <option value="page1">spaCy</option>
            <option value="page2">NLTK</option>
            <option value="page3">TreeTagger</option>
        </select>
        <div id="page1" class="section">
            <table></table>
        </div>
        <div id="page2" class="section" style="display:none;">
            <!-- Insère ici le tableau généré par NLTK -->
        </div>
        <div id="page3" class="section" style="display:none;">
            <!-- Insère ici le tableau généré par TreeTagger -->
        </div>
    </div>
    <script>
        function changePage(page) {
            var sections = document.getElementsByClassName('section');

            for (var i = 0; i < sections.length; i++) {
                sections[i].style.display = 'none';
            }

            document.getElementById(page).style.display = 'block';
        }
    </script>
</body>
</html>
"""

# lxml = analyseur syntaxique (pas besoin de l'importer)
# Il va permettre de modifier le code HTML avec la variable soup
soup = bs(code_html, 'lxml')
table = soup.table

# On modifie les noms de colonnes
nom_colonnes = ["Mot (" + str(corpus_count) + " mots)", 'Lemme', 'POS', 'DEP']
thead = soup.new_tag('thead')
table.append(thead)

tr_head = soup.new_tag('tr')
thead.append(tr_head)

for header in nom_colonnes:
    th = soup.new_tag('th')
    th.string = header
    tr_head.append(th)


# On ajoute aux colonnes le contenu du texte annoté
tbody = soup.new_tag('tbody')
table.append(tbody)

for row in lignes:
    tr = soup.new_tag('tr')
    tbody.append(tr)
    for cell in row:
        td = soup.new_tag('td')
        td.string = cell
        tr.append(td)

# On crée la balise <style> pour insérer du CSS
style = soup.new_tag('style')
style.string = '''
table {
    width: 100%;
    border-collapse: collapse;
    border: 1px solid #ddd;
}

th, td {
    border: 1px solid black;
    padding: 8px;
    text-align: left;
}

th {
    background-color: #f2f2f2;
}
'''

# On ajoute la feuille de style à soup
soup.body.insert(0, style)


# Ici on va gérer l'affichage des 3 tableaux
with open("../index.html", "r") as f:
    content = f.read()
    start_index = content.find('<div id="page1" class="section">') + len('<div id="page1" class="section">')
    end_index = content.find('</div>', start_index)
    content = content[:start_index] + str(soup) + content[end_index:]

with open("../index.html", "w") as resultats:
    resultats.write(content)