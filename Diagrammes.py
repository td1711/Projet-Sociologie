import sqlite3 as sq3
from matplotlib import pyplot as plt
from Fonctions import *

def camembert_professions():
    connexion = sq3.connect('BDD.db')
    curseur = connexion.cursor()
    plt.figure(figsize = (7, 8))
    x = list(professions().values())
    plt.pie(x, labels = list(professions().keys()))
    plt.legend()
    plt.show()
       
def camembert_elus_hommes_femmes():
    """
    Crée un diagramme sous forme de camembert montrant
    la répartition des hommes et des femmes parmi les élus
    """
    connexion = sq3.connect('BDD.db')
    curseur = connexion.cursor()
    #Compte le nombre de femmes élues
    requete = "SELECT count(Id) FROM elus WHERE Sexe = 'F'"
    curseur.execute(requete)
    for t in curseur:
        nbr_femmes = t[0]
    #Compte le nombre d'élues
    requete = "SELECT count(Id) FROM elus"
    curseur.execute(requete)
    for t in curseur:
        nbr_elus = t[0]
        
    #Création du camembert
    plt.figure(figsize = (7, 8))
    x = [nbr_femmes,nbr_elus-nbr_femmes]
    plt.pie(x, labels = ['Nombre de femmes élues',"Nombre total d'hommes élus"])
    plt.legend()
    plt.show()
    
    
def camembert_maire_et_élus():
    """
    Crée un diagramme sous forme de camembert montrant
    la répartition des maires parmi les élus
    """
    #Compte le nombre de maire parmi les élus
    connexion = sq3.connect('BDD.db')
    curseur = connexion.cursor()
    requete = "SELECT count(Id) FROM elus WHERE Fonction = 'Maire'"
    curseur.execute(requete)
    for t in curseur:
        nbr_maires = t[0]
    #Compte le nombre d'élus
    requete = "SELECT count(Id) FROM elus"
    curseur.execute(requete)
    for t in curseur:
        nbr_elus = t[0]
    #Création du camembert
    plt.figure(figsize = (7, 8))
    x = [nbr_maires,nbr_elus-nbr_maires]
    plt.pie(x, labels = ['Nombre de maires',"Nombre d'élus non maire"])
    plt.legend()
    plt.show()
    
def graphique__nbr_elus_pardecennie():
    """
    Renvoie un graphique du nombre d'élus par département
    """
    connexion = sq3.connect('BDD.db')
    curseur = connexion.cursor()
    a = 1929
    b = 1920
    dico = {}
    nombre_decennie = []
    liste_decennies = []
    for i in range(9):
        liste_decennies.append(str(b)+"-"+str(a))
        liste = []
        requete = "SELECT count(*) from elus WHERE substr(Date_naissance, 7)"\
        "<='"+str(a)+"' AND substr(Date_naissance, 7)>='"+str(b)+"'"
        curseur.execute(requete)
        for t in curseur:
            liste.append(t[0])
        a = a + 10
        b = b + 10
        nombre_decennie.append(liste[0])
    
    plt.title("Nombre d'élus par date de naissance")
    listeAbscisses=liste_decennies
    listeOrdonnees=nombre_decennie
    plt.plot(listeAbscisses,listeOrdonnees, label="évolution", color = "red")
    plt.legend()
    plt.grid()
    plt.xlabel("décennies")
    plt.ylabel("nombre de naissance d'élus")
    plt.savefig("AAAAAA.png")
    plt.show()
    
def camembert_maires_hommes_et_femmes():
    connexion = sq3.connect('BDD.db')
    curseur = connexion.cursor()
    requete = "SELECT count(*) from elus WHERE Fonction = 'Maire' AND Sexe = 'M'"
    curseur.execute(requete)
    for t in curseur:
        nbr_maire_hommes = t[0]
    requete = "SELECT count(*) from elus WHERE Fonction = 'Maire' AND Sexe = 'F'"
    curseur.execute(requete)
    for t in curseur:
        nbr_maire_femmes = t[0]
    plt.figure(figsize = (7, 8))
    x = [nbr_maire_hommes,nbr_maire_femmes]
    plt.pie(x, labels = ["Nombre d'hommes maires","Nombre de femmes maires"])
    plt.legend()
    plt.show()
    
    
def camembert_elus_français_et_autres():
    connexion = sq3.connect('BDD.db')
    curseur = connexion.cursor()
    requete = "SELECT count(*) from elus WHERE Nationalite = 'Française'"
    curseur.execute(requete)
    for t in curseur:
        nbr_français = t[0]
    requete = "SELECT count(*) from elus WHERE Nationalite is not 'Française'"
    curseur.execute(requete)
    for t in curseur:
        nbr_autres = t[0]
    requete = "SELECT count(*) from elus"
    curseur.execute(requete)
    for t in curseur:
        nbr_total = t[0]
    plt.figure(figsize = (7, 8))
    x = [nbr_français*100/nbr_total, nbr_autres*100/nbr_total]
    plt.pie(x, labels = ['Elus de nationalité française', "Elus d'une autre nationalité"])
    plt.legend()
    plt.show()

def diagramme_nbr_elus_outre_mer():
    listeX  =  list(nbr_elus_departement().keys())[-8:]
    liste_hommes = [0]*8
    liste_femmes = list(nbr_femmes_elues_departement().values())[-8:]
    liste_total = list(nbr_elus_departement().values())[-8:]
    for i in range(len(liste_total)):
        liste_hommes[i] = liste_total[i] - liste_femmes[i]
    listeY2 = [483, 497, 299, 463, 287, 576, 14, 422]
    plt.bar(listeX, liste_total, width = 0.5, color = "red", label = "Femmes") 
    plt.bar(listeX, liste_hommes, width = 0.5, color = "green", label = "Hommes") 
    plt.legend()
    plt.show()

    
print("Certains graphiques peuvent mettre du temps à se générer")
camembert_professions()
camembert_elus_hommes_femmes()
camembert_maire_et_élus()
graphique__nbr_elus_pardecennie()
camembert_maires_hommes_et_femmes()
camembert_elus_français_et_autres()
diagramme_nbr_elus_outre_mer()