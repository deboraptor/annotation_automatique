import stanza
from sklearn.metrics import precision_score, recall_score, f1_score
from bs4 import BeautifulSoup as bs

from annexe import resultats_norme_moi
from annexe import resultats_non_norme_moi

# Il faut télécharger les corpus en français pour stanza ! Un seul téléchargement suffit
# stanza.download('fr')
nlp = stanza.Pipeline(lang='fr', processors='tokenize,lemma,pos,depparse')

def collecter_texte_norme():
    # Je fais le traitement avec Stanza
    with open("texte_norme.txt") as fichier_corpus:
        corpus = fichier_corpus.read()
        doc = nlp(corpus)
        nb_words = list(corpus.split())
        corpus_count = len(nb_words)

    # Contenu des colonnes
    lignes = []
    resultats_norme_machine = []
    for sentence in doc.sentences:
        for token in sentence.tokens:
            ligne_token = getattr(token, 'text', '')
            ligne_lemme = getattr(token, 'lemma', '')
            ligne_pos = getattr(token, 'pos', '')
            ligne_dep = getattr(token, 'deprel', '')
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

    with open("../page2.html", "r") as fichier_page2_metrique:
        page2_metrique = bs(fichier_page2_metrique.read(), "lxml")

    # Calculer les métriques de précision, rappel et F-mesure
    while len(resultats_norme_machine_bin) < len(resultats_norme_moi_bin):
        resultats_norme_machine_bin.append((0, 0, 0))

    while len(resultats_norme_moi_bin) < len(resultats_norme_machine_bin):
        resultats_norme_moi_bin.append((0, 0, 0))    
    try:
        precision = precision_score(resultats_norme_machine_bin, resultats_norme_moi_bin, average="micro", zero_division=1)
    except ValueError:
        print("Les tableaux resultats_non_norme_machine_bin et resultats_non_norme_moi_bin n'ont pas la même longueur. Le calcul de la métrique de précision est ignoré.")
        precision = None

    precision = precision_score(resultats_norme_machine_bin, resultats_norme_moi_bin, average="micro", zero_division=1)
    rappel = recall_score(resultats_norme_machine_bin, resultats_norme_moi_bin, average="micro", zero_division=1)
    fmesure = f1_score(resultats_norme_machine_bin, resultats_norme_moi_bin, average="micro", zero_division=1)

    tableau_metrique = page2_metrique.find('table', {'id': 'metrique'})

    cellule = tableau_metrique.find('td', {'class': 'rappel_norme'})
    cellule.string = "Rappel : " + str(rappel)
    cellule = tableau_metrique.find('td', {'class': 'precision_norme'})
    cellule.string = "Précision : " + str(precision)
    cellule = tableau_metrique.find('td', {'class': 'fmesure_norme'})
    cellule.string = "F-mesure : " + str(fmesure)

    with open("../page2.html", "w") as fichier_metrique:
        fichier_metrique.write(str(page2_metrique))

    ##################################################################################

    with open("../page2.html", "r") as fichier_page2_tableau:
        page2_tableau = bs(fichier_page2_tableau.read(), "lxml")

    table = page2_tableau.find('table', {'id': 'table1'})

    # On modifie les noms de colonnes
    nom_colonnes = ["Mot (" + str(corpus_count) + " mots)", 'Lemme', 'POS', 'DEP']
    thead = page2_tableau.new_tag('thead')
    table.append(thead)

    tr_head = page2_tableau.new_tag('tr')
    thead.append(tr_head)

    for header in nom_colonnes:
        th = page2_tableau.new_tag('th')
        th.string = header
        tr_head.append(th)

    # On ajoute aux colonnes le contenu du texte annoté
    tbody = page2_tableau.new_tag('tbody')
    table.append(tbody)

    for ligne in lignes:
        tr = page2_tableau.new_tag('tr')
        tbody.append(tr)
        for cell in ligne:
            td = page2_tableau.new_tag('td')
            td.string = cell
            tr.append(td)

    with open("../page2.html", "w") as fichier_page2_tableau:
        fichier_page2_tableau.write(str(page2_tableau))

def collecter_texte_non_norme():
    # Je refais le traitement avec Stanza
    with open("texte_non_norme.txt") as fichier_corpus:
        corpus = fichier_corpus.read()
        doc = nlp(corpus)
        nb_words = list(corpus.split())
        corpus_count = len(nb_words)

    # Contenu des colonnes
    lignes = []
    resultats_non_norme_machine = []
    for sentence in doc.sentences:
        for token in sentence.tokens:
            ligne_token = getattr(token, 'text', '')
            ligne_lemme = getattr(token, 'lemma', '')
            ligne_pos = getattr(token, 'pos', '')
            ligne_dep = getattr(token, 'deprel', '')
            lignes.append([ligne_token, ligne_lemme, ligne_pos, ligne_dep])
            # Je crée une liste de tuples pour que ce soit plus simple à faire la f-mesure
            tuple_res = (ligne_token, ligne_lemme, ligne_pos)
            resultats_non_norme_machine.append(tuple_res)

    # On compare les deux listes pour faire la f-mesure
    resultats_non_norme_machine_bin = []
    resultats_non_norme_moi_bin = [(1, 1, 1) for i in range(len(resultats_norme_moi))]
    for i in range(len(resultats_non_norme_machine)):
        liste_inter = []
        for j in range(len(resultats_non_norme_machine[i])):
            if resultats_non_norme_machine[i][j] == resultats_non_norme_moi[i][j]:
                liste_inter.append(1)
            else:
                liste_inter.append(0)
        resultats_non_norme_machine_bin.append(tuple(liste_inter))

    with open("../page2.html", "r") as fichier_page2_metrique:
        page2_metrique = bs(fichier_page2_metrique.read(), "lxml")

    # Calculer les métriques de précision, rappel et F-mesure
    while len(resultats_non_norme_machine_bin) < len(resultats_non_norme_moi_bin):
        resultats_non_norme_machine_bin.append((0, 0, 0))

    while len(resultats_non_norme_moi_bin) < len(resultats_non_norme_machine_bin):
        resultats_non_norme_moi_bin.append((0, 0, 0))    
    try:
        precision = precision_score(resultats_non_norme_machine_bin, resultats_non_norme_moi_bin, average="micro", zero_division=1)
    except ValueError:
        print("Les tableaux resultats_non_norme_machine_bin et resultats_non_norme_moi_bin n'ont pas la même longueur. Le calcul de la métrique de précision est ignoré.")
        precision = None

    rappel = recall_score(resultats_non_norme_machine_bin, resultats_non_norme_moi_bin, average="micro", zero_division=1)
    fmesure = f1_score(resultats_non_norme_machine_bin, resultats_non_norme_moi_bin, average="micro", zero_division=1)

    tableau_metrique = page2_metrique.find('table', {'id': 'metrique'})

    cellule = tableau_metrique.find('td', {'class': 'rappel_norme'})
    cellule.string = "Rappel : " + str(rappel)
    cellule = tableau_metrique.find('td', {'class': 'precision_norme'})
    cellule.string = "Précision : " + str(precision)
    cellule = tableau_metrique.find('td', {'class': 'fmesure_norme'})
    cellule.string = "F-mesure : " + str(fmesure)

    with open("../page2.html", "w") as fichier_metrique:
        fichier_metrique.write(str(page2_metrique))

    ##################################################################################

    with open("../page2.html", "r") as fichier_page2_tableau:
        page2_tableau = bs(fichier_page2_tableau.read(), "lxml")

    table = page2_tableau.find('table', {'id': 'table1'})

    # On modifie les noms de colonnes
    nom_colonnes = ["Mot (" + str(corpus_count) + " mots)", 'Lemme', 'POS', 'DEP']
    thead = page2_tableau.new_tag('thead')
    table.append(thead)

    tr_head = page2_tableau.new_tag('tr')
    thead.append(tr_head)

    for header in nom_colonnes:
        th = page2_tableau.new_tag('th')
        th.string = header
        tr_head.append(th)

    # On ajoute aux colonnes le contenu du texte annoté
    tbody = page2_tableau.new_tag('tbody')
    table.append(tbody)

    for ligne in lignes:
        tr = page2_tableau.new_tag('tr')
        tbody.append(tr)
        for cell in ligne:
            td = page2_tableau.new_tag('td')
            td.string = cell
            tr.append(td)

    with open("../page2.html", "w") as fichier_page2_tableau:
        fichier_page2_tableau.write(str(page2_tableau))

def main():
    collecter_texte_non_norme()
    collecter_texte_norme()

if __name__ == "__main__":
    main()