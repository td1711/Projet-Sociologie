import sqlite3 as sq3

def nbr_elus_departement():
    """
    Renvoie un dictionnaire contenant
    le nombre d'élus pour chaque département
    """
    connexion = sq3.connect('BDD.db')
    curseur = connexion.cursor()
    departements = liste_departements()   
    liste = []
    #Permet de chercher le nombre d'élus pour chaque
    #département et de l'ajouter dans une liste
    for departement in departements:
        requete = "SELECT COUNT(Nom_elu) FROM elus WHERE "\
        "Code_dpt = "+"'"+departement+"'"+""
        curseur.execute(requete)
        for t in curseur:
            liste.append(t[0])
    curseur.close()
    connexion.close()
    #Création du dictionnaire
    dico = {}
    for i in range(len(liste)):
        dico[departements[i]] = liste[i]
    return dico

def liste_departements():
    """
    Renvoie une liste contenant tous les codes des départements
    """
    connexion = sq3.connect('BDD.db')
    curseur = connexion.cursor()
    requete = "SELECT Code_dpt FROM departement"
    curseur.execute(requete)
    departements = []
    chiffres = ['1','2','3','4','5','6','7','8','9']
    for t in curseur:
        if str(t[0]) in chiffres:
            departements.append("0"+str(t[0]))
        else:
            departements.append(str(t[0]))
    curseur.close()
    return departements

def nbr_femmes_elues_departement():
    """
    Renvoie un dictionnaire contenant le nombre
    de femmes élues pour chaque département
    """
    connexion = sq3.connect('BDD.db')
    curseur = connexion.cursor()
    departements = liste_departements()   
    liste = []
    #Permet de chercher le nombre de femmes élues pour
    #chaque département et de l'ajouter dans une liste
    for departement in departements:
        requete = "SELECT count(Nom_elu) FROM elus WHERE Sexe = 'F' "\
        "and Code_dpt = "+"'"+departement+"'"+""
        curseur.execute(requete)
        for t in curseur:
            liste.append(t[0])
    curseur.close()
    connexion.close()
    #Création du dictionnaire
    dico = {}
    for i in range(len(liste)):
        dico[departements[i]] = liste[i]
    return dico

def moyenne_age():
    """
    Renvoie la moyenne d'âge de tous les élus
    """
    connexion = sq3.connect('BDD.db')
    curseur = connexion.cursor()
    requete = "SELECT Date_naissance FROM elus WHERE Code_dpt = '2A' OR Code_dpt = '2B'"
    curseur.execute(requete)
    dates = []
    #Permet d'ajouter les années de naissance de chaque élus dans la liste dates
    for t in curseur:
        date = str(t[0])
        date = date_en_annee(date)
        dates.append(int(date))
    somme = 0
    #Calcul de la moyenne
    for date in dates:
        somme = somme + date
    return 2020 - round(somme / len(dates))

def date_en_annee(date):
    """
    Renvoie l'année d'une date de naissance de la forme "JJ/MM/AAAA"
    """
    l = date.split("/")
    return l[2]

def moyenne_age_departement():
    """
    Renvoie un dictionnaire contenant la moyenne
    d'âge de tous les élus par département
    """
    connexion = sq3.connect('BDD.db')
    curseur = connexion.cursor()
    departements = liste_departements()
    dico = {}
    liste_date_elus_departements = []
    a = ['2A','2B','ZA','ZB','ZC','ZD','ZM','ZP','ZS','ZN']
    #Permet de parcourir tous les départements
    for departement in departements:
        if departement not in a:
            requete = "SELECT Date_naissance FROM elus WHERE Code_dpt = "+departement+""
        else:
            requete = "SELECT Date_naissance FROM elus WHERE "\
            "Code_dpt = "+"'"+departement+"'"+""
        curseur.execute(requete)
        #Ajoute dans la liste toutes les années
        #de naissance des élus du département
        liste = []
        for t in curseur:
            liste.append(date_en_annee(t[0]))
        #La liste liste_date_elus_departements contient toutes les
        #années de naissance des élus triées par département
        liste_date_elus_departements.append(liste)
    #Permet de parcourir chaque liste des dates de naissances des départements
    i = 0
    for departement in liste_date_elus_departements:
        somme = 0
        #Permet d'ajouter dans somme les années de naissance des élus du département
        for date_elu in departement:
            somme = somme + int(date_elu)
        liste_date_elus_departements[i] = 2020-round(somme / len(departement))
        i = i+1
    #Création du dictionnaire contenant les moyennes d'âge par département
    i = 0
    for age in liste_date_elus_departements:
        dico[departements[i]] = age
        i = i+1
    return dico

def professions():
    """
    Renvoie un dictionnaire contenant les
    profession les plus courantes parmi les élus
    """
    connexion = sq3.connect('BDD.db')
    curseur = connexion.cursor()
    requete = "SELECT Code_profession FROM profession"
    curseur.execute(requete)
    #Création d'une liste contenant tous les code_profession
    professions = []
    for t in curseur:
        professions.append(str(t[0])) 
    dico = {}
    #Permet de parcourir chaque profession et
    #de compter le nombre d'élus qui la pratique
    for profession in professions:
        requete = "SELECT COUNT(Nom_elu) FROM elus "\
        "WHERE Code_profession = "+"'"+profession+"'"+""
        curseur.execute(requete)
        liste = []
        for t in curseur:
            liste.append(t[0])
        dico[profession] = liste[0]
    
    #Permet de compter le nombre d'élus
    somme = 0
    for valeur in dico.values():
        somme = somme + valeur
    nombres_elus_profession = somme
    
    #Permet de sélectionner les 10 professions les plus pratiquées par les élus
    dico_premiers = {}
    for i in range(10):
        maxi = 0
        maxi_profession = ""
        for item in dico:
            if dico[item] > maxi:
                requete = "SELECT Profession FROM profession WHERE Code_profession ="+item+""
                curseur.execute(requete)
                for t in curseur:
                    profession = str(t[0])
                maxi = dico[item]
                maxi_profession = profession
                maxi_profession_code = item
        dico_premiers[maxi_profession] = maxi
        del dico[maxi_profession_code]
    
    #Permet de compter le nombre d'élus qui ne
    #pratiquent pas les 10 professions les plus courantes
    somme = 0
    for valeur in dico_premiers.values():
        somme = somme + valeur
    nbr_autres = nombres_elus_profession - somme
    dico_premiers['Autres'] = nbr_autres
    return dico_premiers

def prenoms_courants_par_decennie():
    """
    Renvoie les prénoms les plus courants par décennie
    """
    connexion = sq3.connect('BDD.db')
    curseur = connexion.cursor()
    maxi_prenoms = []
    a = 1919
    b = 1910
    dico = {}
    liste_genre = ["M","F"] 
    #Permet de trouver la décennie la plus ancienne et la plus récente
    requete = "SELECT min(substr(Date_naissance, 7)),"\
    "max(substr(Date_naissance, 7)) FROM elus "
    curseur.execute(requete)
    for t in curseur:
        mini = int(t[0])
        maxi = int(t[1])
    mini = mini-mini%10
    maxi = maxi-maxi%10
    print("Prévoir au moins 5 minutes d'attente...")
    #La boucle parcourt les différentes décennies
    for i in range(((maxi-mini+10)//10)*2):
        print(str(round((i/18)*100,1))+"%"+ " : " +str(b)+'-'+str(a))
        #La décennie change que lorsque i est pair afin de faire les prénoms
        #masculins (i pair) et féminins ( impair)
        if i%2 == 0:
            liste_decennie = []
            a = a + 10
            b = b + 10
        #Cherche les prénoms dans la décennie
        requete = "SELECT Prenom_elu from elus WHERE substr(Date_naissance, 7)<='"\
        +str(a)+"' AND substr(Date_naissance, 7)>='"+str(b)+\
        "'AND Sexe = '"+liste_genre[i%2]+"'"
        
        curseur.execute(requete)
        prenoms = []
        for t in curseur:
            prenoms.append(t[0])
        maxi = 0
        liste = []
        #Cherche le(s) prénom(s) le(s) plus courant(s) de la décennie
        for prenom in prenoms:
            if prenom not in liste:
                occurence = prenoms.count(prenom)
                if occurence > maxi:
                    maxi = occurence
                    liste = [prenom]
                elif occurence == maxi:
                    liste.append(prenom)
        liste_decennie.append(liste)
        if i%2 == 1:
            dico[str(b)+"-"+str(a)] = liste_decennie
    return dico

def dico_code_profession():
    """
    Renvoie un dictionnaire ayant comme clés les codes professions
    et comme valeurs les noms des professions
    """
    connexion = sq3.connect('BDD.db')
    curseur = connexion.cursor()
    dico = {}
    requete = "SELECT Code_profession, Profession from profession"
    curseur.execute(requete)
    for t in curseur:
        dico[t[0]] = t[1]
    return dico

def profession_par_decennie():
    """
    Renvoie la/les profession(s) la/les plus courante(s) par décennie
    """
    connexion = sq3.connect('BDD.db')
    curseur = connexion.cursor()
    requete = "SELECT min(substr(Date_naissance, 7)),"\
    "max(substr(Date_naissance, 7)) FROM elus "
    curseur.execute(requete)
    for t in curseur:
        mini = int(t[0])
        maxi = int(t[1])
    dico = {}
    #Boucle permettant de parcourir les décennies,
    #i représentant le début de la décennie
    print("Prévoir au moins 5 minutes d'attente...")
    for i in range(mini-mini%10, maxi + 10-maxi%10-1,10):
        print(i,i+9)
        requete = "SELECT Code_profession FROM elus WHERE substr(Date_naissance, 7)"\
        "<='"+str(i+9)+"' AND substr(Date_naissance, 7)>='"+str(i)+"'"
        curseur.execute(requete)
        codes = []
        for t in curseur:
            codes.append(t[0])
        liste = []
        plus_grand = 0
        #Permet de cherche la profession la plus courante dans la décennie
        for code in codes:
            if code not in liste:
                occurence = codes.count(code)
                if occurence > plus_grand:
                    plus_grand = occurence
                    liste = [code]
                elif occurence == plus_grand:
                    liste.append(code)
        dico[str(i)+"-"+str(i+9)] = liste
        
    dico_code_prof = dico_code_profession()
    for cle in dico:
        dico[cle] = dico_code_prof[dico[cle][0]]
    return dico


#print(prenoms_courants_par_decennie())
#print(profession_par_decennie())