import spacy
from sklearn.metrics import precision_score, recall_score, f1_score
from bs4 import BeautifulSoup as bs

from annexe import resultats_norme_moi
from annexe import resultats_non_norme_moi

def collecter_texte_norme():
    # Je fais le traitement avec spaCy
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
    
    ##################################################################################

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
        
def collecter_texte_non_norme():
    # On refait le traitement avec spaCy
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
        
    with open("../page1.html", "r") as fichier_page1_tableau_non_nome:
        page1_tableau_non_nome = bs(fichier_page1_tableau_non_nome.read(), "lxml")

    table = page1_tableau_non_nome.find('table', {'id': 'table2'})

    # On modifie les noms de colonnes
    nom_colonnes = ["Mot (" + str(corpus_count_non_norme) + " mots)", 'Lemme', 'POS', 'DEP']
    thead = page1_tableau_non_nome.new_tag('thead')
    table.append(thead)

    tr_head = page1_tableau_non_nome.new_tag('tr')
    thead.append(tr_head)

    for header in nom_colonnes:
        th = page1_tableau_non_nome.new_tag('th')
        th.string = header
        tr_head.append(th)

    # On ajoute aux colonnes le contenu du texte annoté
    tbody = page1_tableau_non_nome.new_tag('tbody')
    table.append(tbody)

    for ligne in lignes:
        tr = page1_tableau_non_nome.new_tag('tr')
        tbody.append(tr)
        for cell in ligne:
            td = page1_tableau_non_nome.new_tag('td')
            td.string = cell
            tr.append(td)
    
    with open("../page1.html", "w") as fichier_page1_tableau_non_nome:
        fichier_page1_tableau_non_nome.write(str(page1_tableau_non_nome))

def main():
    collecter_texte_non_norme()
    collecter_texte_norme()

if __name__ == "__main__":
    main()