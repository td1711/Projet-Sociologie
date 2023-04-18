from Fonctions import *

def Lancer_carte_tkinter():
    """
    Permet de créer et de générer la carte des départements grâce
    à la fonction tkinter()
    """
    import webbrowser
    noms = tkinter()
    liste_informations = []
    #Parcout les différents noms possibles dans la liste noms et
    #exécute la fonction correspondant au nom
    #Puis ajoute les informations dans la liste liste_informations
    if noms != None:
        print("Veuillez patienter...")
        if "Nombre elus" in noms:
            print(str(round(noms.index("Nombre elus")/len(noms)*100,1))+" %")
            nbr_elus = nbr_elus_departement()
            liste_informations.append(nbr_elus)
        if "Nombre de femmes elues" in noms:
            print(str(round(noms.index("Nombre de femmes elues")/len(noms)*100,1))+" %")
            nbr_femmes_elues = nbr_femmes_elues_departement()
            liste_informations.append(nbr_femmes_elues)
        if "Moyenne d'age des elus" in noms:
            print(str(round(noms.index("Moyenne d'age des elus")/len(noms)*100,1))+" %")
            moyenne_age = moyenne_age_departement()
            liste_informations.append(moyenne_age)
        print("100 %")
        fichier = "departements.geojson"
        i = 0
        #Parcours les dictionnaires dans la liste informations pour
        #les ajouter sur la carte avec la fonction
        for dico in liste_informations:
            ajouter_information_carte_departements(fichier,dico,noms[i])
            fichier = "nouvelle_carte.geojson"
            i = i + 1
        charger_carte("nouvelle_carte.geojson",noms)
        webbrowser.open("Carte_departements.html")

def charger_carte(fichier,liste_informations):
    """
    Sauvegarde une carte en html à partir d'un fichier geojson et d'une liste
    contenant les informations présentes dans le fichier
    """
    import folium
    GEOJSON = fichier
    m = folium.Map(location=[46.9881194908,3.15689130958],zoom_start=6)
    fc = folium.GeoJson(
        GEOJSON,
        name='geojson'
    ).add_to(m)

    fc.add_child(folium.features.GeoJsonTooltip\
    (fields=["code","nom"] + liste_informations))

    folium.LayerControl().add_to(m)
    m.save('Carte_departements.html')


def ajouter_information_carte_departements(fichier,dico_information,nom):
    """
    Permet d'ajouter une nouvelle valeur par département
    à afficher sur la carte à partir d'un fichier geojson
    -dico_information doit contenir les codes des départements
    en clé et en valeurs les informations pour chaque département
    -nom représente le nom à afficher pour chaque département
    devant chaque valeur du dictionnaire, ex : 'nom departement'
    """
    f = open(fichier,"r",encoding = "utf-8")
    contenu = f.read()
    f.close()
    #Le contenu du fichier est mis sous forme de liste pour
    #insérer plus facilement les informations au bon endroit
    liste = contenu.split('"')
    outremer = ['ZA','ZB','ZC','ZD','ZM','ZP','ZS','ZN']
    #Permet de parcourir chaque département
    for item in dico_information:
        if item not in outremer:
            #On cherche la position du département dans le fichier
            index = liste.index(item)
            #On insère le nom puis la valeur pour chaque département
            liste.insert(index + 5,',"'+nom+'":"'+str(dico_information[item])+'')
    contenu = '"'.join(liste)
    #Enfin, on copie le contenu modifié dans un nouveau fichier
    fichier = open('nouvelle_carte.geojson',"w",encoding = "utf-8")
    fichier.write(contenu)
    fichier.close()
    return 'nouvelle_carte.geojson'

def tkinter():
    '''
    Permet de créer une fenêtre tkinter pour choisir les informations à
    mettre sur la carte lors de l'exécution de la fonction Lancer_carte_tkinter()
    '''
    import tkinter
    from tkinter import ttk
    #Création de la fenêtre
    root= tkinter.Tk()
    root.geometry("800x600") 
    root.title("Une fenetre")
    root.resizable(width = False, height = False)
    root.configure(bg = "#575E6B")
    
    #fonction utilisée en appuyant sur le bouton générer permettant
    #de sauvegarder dans une liste les choix sélectionnées
    def confirmer():
        global liste_coches
        liste_coches = []
        for i in range(len(valeurs_cases)):
            liste_coches.append(valeurs_cases[i].get())
        root.destroy()
        return liste_coches
    
    noms = ["Nombre elus", "Nombre de femmes elues", "Moyenne d'age des elus"]
    cases = {}
    #Permet de placer les boutons sur la fenêtre
    valeurs_cases = [tkinter.IntVar() for i in range(len(noms))]
    for i in range(len(noms)):
        c = tkinter.Checkbutton(root, variable = valeurs_cases[i], text = noms[i])
        c.place(x = 20, y = 40 + i * 35)
        cases[noms[i]] = c
        
    Texte = tkinter.Label(text = "Chosir les catégories"\
    " à afficher sur la carte des départements :")
    Texte.place(x=10,y=10)
    
    bouton = tkinter.Button(root,text = "Générer la carte"\
    , width = 25, height = 3, command = confirmer)
    bouton2 = tkinter.Button(root, text='Quitter', command=root.destroy)
    bouton.place(x=10,y= 100 + i * 35)
    bouton2.place(x=750,y=10)
    root.mainloop()
    dico_noms = {}
    #Si la liste_coches n'est pas vide, permet de convertir les 0 de la liste
    #en une liste des noms
    try:
        for i in range(len(liste_coches)):
            dico_noms[noms[i]] = liste_coches[i]
        noms = []
        cles = list(dico_noms.keys())
        for i in range(len(dico_noms)):
            if dico_noms[cles[i]] == 0:
                del(dico_noms[cles[i]])
            else:
                noms.append(cles[i])
        return noms
    except:
        pass

Lancer_carte_tkinter()