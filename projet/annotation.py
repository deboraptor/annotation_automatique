import spacy
from sklearn.metrics import precision_score, recall_score, f1_score
from bs4 import BeautifulSoup as bs

from annexe import resultats_norme_moi
from annexe import resultats_non_norme_moi

def collecter_page1():
    # Je fais le traitement avec spaCypy
    with open("texte_norme.txt") as fichier_corpus:
        nlp = spacy.load("fr_core_news_sm")
        corpus = fichier_corpus.read()
        doc = nlp(corpus)
        nb_words = list(corpus.split())
        corpus_count = len(nb_words)

    # Contenu des colonnes
    lignes = []
    resultats_norme_machine = []
    for token in doc:
        ligne_token = token.text
        ligne_lemme = token.lemma_
        ligne_pos = token.pos_
        ligne_dep = token.dep_
        lignes.append([ligne_token, ligne_lemme, ligne_pos, ligne_dep])
        # Je crée une liste de tuples pour que ce soit plus simple à faire la f-mesure
        tuple_res = (ligne_token, ligne_lemme, ligne_pos)
        resultats_norme_machine.append(tuple_res)
    # print(resultats_norme_machine)
            
    # On compare les deux listes pour faire la f-mesure
    resultats_norme_machine_bin = []
    resultats_norme_moi_bin = [(1, 1, 1) for i in range(len(resultats_norme_moi))]
    for i in range(len(resultats_norme_machine)):
        liste_inter = []
        for j in range(len(resultats_norme_machine[i])):
            if resultats_norme_machine[i][j] == resultats_norme_moi[i][j]:
                liste_inter.append(1)
            else:
                liste_inter.append(0)
        resultats_norme_machine_bin.append(tuple(liste_inter))
    
    with open("../page1.html", "r") as fichier_page1_metrique:
        page1_metrique = bs(fichier_page1_metrique.read(), "lxml")

    # Calculer les métriques de précision, rappel et F-mesure
    precision = precision_score(resultats_norme_machine_bin, resultats_norme_moi_bin, average="micro", zero_division=1)
    rappel = recall_score(resultats_norme_machine_bin, resultats_norme_moi_bin, average="micro", zero_division=1)
    fmesure = f1_score(resultats_norme_machine_bin, resultats_norme_moi_bin, average="micro", zero_division=1)

    tableau_metrique = page1_metrique.find('table', {'id': 'metrique'})

    cellule = tableau_metrique.find('td', {'class': 'rappel_norme'})
    cellule.string = "Rappel : " + str(rappel)
    cellule = tableau_metrique.find('td', {'class': 'precision_norme'})
    cellule.string = "Précision : " + str(precision)
    cellule = tableau_metrique.find('td', {'class': 'fmesure_norme'})
    cellule.string = "F-mesure : " + str(fmesure)

    with open("../page1.html", "w") as fichier_metrique:
        fichier_metrique.write(str(page1_metrique))
    
    ##############################

    with open("../page1.html", "r") as fichier_page1_tableau:
        page1_tableau = bs(fichier_page1_tableau.read(), "lxml")

    table = page1_tableau.find('table', {'id': 'table1'})

    # On modifie les noms de colonnes
    nom_colonnes = ["Mot (" + str(corpus_count) + " mots)", 'Lemme', 'POS', 'DEP']
    thead = page1_tableau.new_tag('thead')
    table.append(thead)

    tr_head = page1_tableau.new_tag('tr')
    thead.append(tr_head)

    for header in nom_colonnes:
        th = page1_tableau.new_tag('th')
        th.string = header
        tr_head.append(th)

    # On ajoute aux colonnes le contenu du texte annoté
    tbody = page1_tableau.new_tag('tbody')
    table.append(tbody)

    for ligne in lignes:
        tr = page1_tableau.new_tag('tr')
        tbody.append(tr)
        for cell in ligne:
            td = page1_tableau.new_tag('td')
            td.string = cell
            tr.append(td)
    
    with open("../page1.html", "w") as fichier_page1_tableau:
        fichier_page1_tableau.write(str(page1_tableau))
        




def collecter_soup_non_norme():
    with open("texte_non_norme.txt") as fichier_corpus_non_norme:
        nlp = spacy.load("fr_core_news_sm")
        corpus_non_norme = fichier_corpus_non_norme.read()
        doc = nlp(corpus_non_norme)
        nb_words_non_norme = list(corpus_non_norme.split())
        corpus_count_non_norme = len(nb_words_non_norme)

    # Contenu des colonnes
    lignes = []
    resultats_non_norme_machine = []
    for token in doc:
        ligne_token = token.text
        ligne_lemme = token.lemma_
        ligne_pos = token.pos_
        ligne_dep = token.dep_
        lignes.append([ligne_token, ligne_lemme, ligne_pos, ligne_dep])
        # Je crée une liste de tuples pour que ce soit plus simple à faire la f-mesure
        tuple_res = (ligne_token, ligne_lemme, ligne_pos)
        resultats_non_norme_machine.append(tuple_res)

    # On compare les deux listes pour faire la f-mesure
    resultats_non_norme_machine_bin = []
    resultats_non_norme_moi_bin = [(1, 1, 1) for i in range(len(resultats_non_norme_moi))]
    for i in range(len(resultats_non_norme_machine)):
        liste_inter = []
        for j in range(len(resultats_non_norme_machine[i])):
            if resultats_non_norme_machine[i][j] == resultats_non_norme_moi[i][j]:
                liste_inter.append(1)
            else:
                liste_inter.append(0)
        resultats_non_norme_machine_bin.append(tuple(liste_inter))

    # Calculer les métriques de précision, rappel et F-mesure
    precision = precision_score(resultats_non_norme_machine_bin, resultats_non_norme_moi_bin, average="micro", zero_division=1)
    rappel = recall_score(resultats_non_norme_machine_bin, resultats_non_norme_moi_bin, average="micro", zero_division=1)
    fmesure = f1_score(resultats_non_norme_machine_bin, resultats_non_norme_moi_bin, average="micro", zero_division=1)

    with open("../page1.html", "r") as fichier_page1_metrique:
        page1_metrique = bs(fichier_page1_metrique.read(), "lxml")

    tableau_metrique = page1_metrique.find('table', {'id': 'metrique'})

    cellule = tableau_metrique.find('td', {'class': 'rappel_non_norme'})
    cellule.string = "Rappel : " + str(rappel)
    cellule = tableau_metrique.find('td', {'class': 'precision_non_norme'})
    cellule.string = "Précision : " + str(precision)
    cellule = tableau_metrique.find('td', {'class': 'fmesure_non_norme'})
    cellule.string = "F-mesure : " + str(fmesure)

    with open("../page1.html", "w") as fichier_metrique:
        fichier_metrique.write(str(page1_metrique))


    ##################################################################################
        
    # # Là je modifie le code html pour mettre des modifications CSS notamment
    # code_html= """
    # <html>
    # <head>
    #     <meta charset="UTF-8">
    #     <title>Annotation automatique : résultats</title>
    #     <meta name="viewport" content="width=device-width, initial-scale=1.0">
    #     <meta http-equiv="X-UA-Compatible" content="ie=edge">
    #     <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bulma@0.9.3/css/bulmaswatch.min.css">
    #     <link rel="stylesheet" href="https://unpkg.com/bulmaswatch/pulse/bulmaswatch.min.css">
    #     <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/bulma/0.9.3/css/bulmaswatch.min.css">
    #     <script defer src="https://use.fontawesome.com/releases/v5.0.10/js/all.js"></script>
    #     <script src="https://code.jquery.com/jquery-3.5.1.min.js"></script>
    #     <script src="index.js"></script>
    # </head>
    # <body>
    #     <div>
    #         <label for="pages">Choisir un module : </label>
    #         <select id="pages" onchange="changePage(this.value)">
    #             <option value="page1">Texte non normé</option>
    #             <option value="page2">Texte normé</option>
    #         </select>
    #         <div id="page1" class="section">
    #             <table></table>
    #         </div>
    #         <div id="page2" class="section">
    #             <table></table>
    #         </div>
    #     </div>
    #     <script>
    #         function changePage(page) {
    #             var sections = document.getElementsByClassName('section');

    #             document.getElementById(page).style.display = 'block';
    #         }
    #     </script>
    # </body>
    # </html>
    # """

    # soup_non_norme = bs(code_html, 'lxml')
    # table = soup_non_norme.table

    # # On modifie les noms de colonnes
    # nom_colonnes = ["Mot (" + str(corpus_count_non_norme) + " mots)", 'Lemme', 'POS', 'DEP']
    # thead = soup_non_norme.new_tag('thead')
    # table.append(thead)

    # tr_head = soup_non_norme.new_tag('tr')
    # thead.append(tr_head)

    # for header in nom_colonnes:
    #     th = soup_non_norme.new_tag('th')
    #     th.string = header
    #     tr_head.append(th)

    # # On ajoute aux colonnes le contenu du texte annoté
    # tbody = soup_non_norme.new_tag('tbody')
    # table.append(tbody)

    # for ligne in lignes:
    #     tr = soup_non_norme.new_tag('tr')
    #     tbody.append(tr)
    #     for cell in ligne:
    #         td = soup_non_norme.new_tag('td')
    #         td.string = cell
    #         tr.append(td)

    # On crée la balise <style> pour insérer du CSS
    # style = soup_non_norme.new_tag('style')
    # style.string = '''
    # table {
    #     width: 100%;
    #     border-collapse: collapse;
    #     border: 1px solid #ddd;
    # }

    # th, td {
    #     border: 1px solid black;
    #     padding: 8px;
    #     text-align: left;
    # }

    # th {
    #     background-color: #f2f2f2;
    # }
    # '''

    # On ajoute la feuille de style à page1
    # soup_non_norme.body.insert(0, style)

    # return soup_non_norme

def main():
    # with open("../index.html", "r") as f:
    #     contenu = f.read()

    soup_non_norme = collecter_soup_non_norme()
    page1 = collecter_page1()

    # Pour les deux tableaux, on va remplacer ce qu'il y a dans les balises <div> par nos tableaux
    # start_index_norme = contenu.find('<div id="page1" class="section">') + len('<div id="page1" class="section">')
    # end_index_norme = contenu.find('</div>', start_index_norme)
    # contenu = contenu[:start_index_norme] + str(page1) + contenu[end_index_norme:]

    # start_index_non_norme = contenu.find('<div id="page2" class="section">') + len('<div id="page2" class="section">')
    # end_index_non_norme = contenu.find('</div>', start_index_non_norme)
    # contenu = contenu[:start_index_non_norme] + str(soup_non_norme) + contenu[end_index_non_norme:]

    # with open("../index.html", "w") as resultats:
    #     resultats.write(contenu)

if __name__ == "__main__":
    main()