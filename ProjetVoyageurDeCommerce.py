"""
ALGORITHME GENETIQUE APPLIQUE AU PROBLEME DU VOYAGEUR DE COMMERCE

TERMINALE NSI 
2020/2021
LYCEE MARC BLOCH

GROUPE:
    - AZIZ Maissa
    - ACIKBAS Tuna
    - FAHEM Rayene
    - GEOFFROY Alexandre    
    - REZKI Saber
    - SCHLEE Adam
    - SIEBERING Juliette
    - TORES CORTEZ Shéridan
    - XAYAPHOUMMINE Aurélie

"""

from tkinter import *
from tkinter.messagebox import *
import os
import ast
import sys
import random
import matplotlib.pyplot as plt
from math import ceil, floor, inf, sqrt
from copy import deepcopy
#-----------------------------------------VARIABLES----------------------------------------------#
ScoreListe = []
NbGenerationTotalListe= []
DicoVilles = {}
NbGeneration = 0
NbGenerationTotal = 0
h = 0
Score = inf
Continue = True
Best = False
NbGenMax = 100

NbIndividus = 100   # Valeur par défaut pour l'initialisation des variables
NbMutation = 50     # - - - - - - - - -
NbHybr = 45         # - - - - - - - - -
NbEug = 5           # - - - - - - - - -
NbRang = 30         # - - - - - - - - -
NbRoul = 15         # - - - - - - - - -
#------------------------------------------------------------------------------------------------#

#-----------------------------------------FONCTIONS----------------------------------------------#

def AfficherInterface():
    """
    Spécification :
    
        Entrée: Aucune

        Sortie: Dictionnaire de villes
                Ex : { '1':(x,y), '2':(x,y), '3':(x,y),
                       '4':(x,y), '5':(x,y), '6':(x,y) }
                       Avec x et y les coordonnées de la ville.

        Rôle:   L'utilisateur clique sur n lieux au hasard qui seront les différentes villes.
                Le programme enregistre les coordonnées des villes dans un dictionnaire.
                Le nom des villes est arbitraire.
        
        Auteurs: ACIKBAS Tuna et XAYAPHOUMMINE Aurélie 
    """
    fenetre = Tk()                                                      # Création de la fenêtre principale.
    fenetre.geometry("600x450+50+10")                                   # Dimensionne et positionne la fenêtre.
    fenetre.title("Voyageur de commerce")                               # Titre de la fenêtre.
    fenetre.configure(bg='MistyRose4')                                  # Donne la couleur de fond de la fenêtre.
    fenetre.resizable(width=False, height=False)                        # Empêche le redimensionnement de la fenêtre.
    photo = PhotoImage(file="carte.png")                                # Récupération de la carte (grâce à le création du fichier carte.png).
    canvas = Canvas(fenetre,width=550, height=382)                      # Définit la taille du canvas contenant la carte.
    canvas.create_image(0, 0, anchor=NW, image=photo)                   # Place la carte sur le canvas.
    
    label = Label(fenetre, text="")
    label.config(bg='MistyRose4')
    label.pack()

    try:                                                                # Vérifie si le fichier Save.csv existe.
        f = open("Save.csv", "r+")
        f.close()
    except:
        f = open("Save.csv", "w+")                                      # Sinon le fichier est créé.
        f.writelines("{}")
        f.close()

    def Clic(event):
        """ Gestion de l'événement Clic gauche sur la zone graphique """
        global h
        X = event.x                                                     # Position du pointeur de la souris.
        Y = event.y
        r = 5
        canvas.create_rectangle(X-r, Y-r, X+r, Y+r, outline='black',fill='red')
        h +=1
        DicoVilles[h]=(X,Y)
        return h

    def Effacer():
        """ Efface tous les points sur la carte"""
        canvas.delete('all')
        canvas.create_image(0, 0, anchor=NW, image=photo)
        global h,DicoVilles
        DicoVilles = {}
        h = 0

    def Save():
        """ Sauvegarde des points que l'utilsateur a donnés"""
        f = open('Save.csv', 'w')
        f.truncate()
        f.writelines(str(DicoVilles))
        f.close()

    def Load():
        global h
        f = open('Save.csv', 'r')
        if os.path.getsize("Save.csv") <= 2:
            showerror("Erreur","Aucun point n'a été sauvegardé, le fichier de sauvegarde est vide.")
        else:
            Dicotemp = ast.literal_eval(f.readline())
            last = h
            for cle, val in Dicotemp.items():
                X=val[0]
                Y=val[1]
                r = 5
                canvas.create_rectangle(X-r, Y-r, X+r, Y+r, outline='black',fill='red')

                if (X,Y) not in DicoVilles.values():

                    DicoVilles[cle + h] = (X,Y)
                    last = cle + h
            h = last
            f.close()
            Save()


    def Next():
        if len(DicoVilles) < 4:
            showerror("Erreur","Vous devez placer au moins 4 points sur la carte !") # Si NbPoints < 3, la mutation et l'hybridation ne fonctionne pas
        else:
            f = open("Save.csv","r")
            Dicotemp = ast.literal_eval(f.readline())
            if DicoVilles != Dicotemp:
                Save()
                fenetre.destroy()
                f.close()
                return DicoVilles 
            else:
                fenetre.destroy()
                f.close()
                return DicoVilles 

    def Back():
        try:
            BoutonAEffacer = DicoVilles.popitem()
            if len(DicoVilles) == 0:
                Save()
                Effacer()
                Save()
            else:
                Save()
                Effacer()
                Load()
                Save()
        except KeyError:
            showerror("Erreur","Il n'y a aucun point sur la carte !")

    canvas.focus_set()

    if canvas.bind("<Button-1>", Clic) == True:                          # Gère le clic sur la carte.
        global h
        h +=1
        canvas.bind("<Button-1>", Clic)

    canvas.pack()

    BoutonEffacer = Button(fenetre, text ='Effacer', command = Effacer, bg="lightblue", relief="raised", overrelief="sunken")
    BoutonEffacer.pack(side = LEFT, padx = 5, pady = 5)                  # Ce bouton efface tout ce qu'il y a sur la carte.

    BoutonSave=Button(fenetre, text="Save", command= Save, bg="honeydew4",fg='red', relief="raised", overrelief="sunken")
    BoutonSave.pack(side=LEFT, padx=5, pady=5)

    BoutonLoad=Button(fenetre, text="Load", command= Load, bg="honeydew4",fg='green2', relief="raised", overrelief="sunken")
    BoutonLoad.pack(side= LEFT, padx=5, pady=5)

    BoutonNext  = Button(fenetre, text="Next", command= Next, bg="firebrick2", relief="raised", overrelief="sunken")
    BoutonNext.pack(side= RIGHT, padx=5, pady=5)

    BoutonBack = Button(fenetre, text= "Back", command = Back,bg ="honeydew4",fg='blue2', relief= "raised", overrelief= "sunken")
    BoutonBack.pack(side= LEFT, padx =5, pady=5)

    fenetre.protocol("WM_DELETE_WINDOW",sys.exit)

    fenetre.mainloop()

    return DicoVilles

def ModifierNbIndividu():
    """
    Spécification :
    
        Entrée: Villes -> dict
                Ex :{ '1':(x,y), '2':(x,y), '3':(x,y),
                      '4':(x,y), '5':(x,y), '6':(x,y) }
                    Avec x et y les coordonnées de la ville et 1,2,3,... le nom des villes.

        Sortie: Aucune (Modifie la variable globale NbIndividus)

        Rôle:   L'utilisateur choisit le nombre d'individu(s) de la population (NbIndividus). 
        
        Auteur: SCHLEE Adam
    """    

    root = Tk()
    root.title("Paramètres de stratégie")
    root.resizable(width=False, height=False)                        # Empêche le redimensionnement de la fenêtre.
    root.configure(bg='MistyRose4')                                  # Donne la couleur de fond de la fenêtre.
    
    def SetNbInd():
        global NbIndividus
        NbIndividus = NbIndividusVar.get()
        root.destroy()
        

    NbIndividusVar = IntVar(value = NbIndividus)
    NbIndividusLabel = Label(root, text = "Nombre d'individus :",bg = "MistyRose4",fg="MistyRose1", font=('Helvetica',12))
    NbIndividusEntry = Entry(root, textvariable = NbIndividusVar, width =50, bg = "MistyRose4",fg="MistyRose1", font=('Helvetica',12))
    BoutonNext = Button(root, text ="Next", bg="firebrick1", command = SetNbInd, relief="raised", overrelief="sunken")

    NbIndividusLabel.grid(row =1, column = 0, padx=5, pady=5)
    NbIndividusEntry.grid(row =1, column = 1, padx=5, pady=5)
    BoutonNext.grid(row =2, columnspan=2, sticky="e", padx=5, pady=5)

    root.mainloop()

def ModifierParamSelection():
    """
    Spécification :
    
        Entrée: Aucune

        Sortie: Aucune (Modifie les variables globales NbEug, NbRang et NbRoul)

        Rôle:   L'utilisateur choisit le nombre de selection(s) par eugénisme, rang et roulette (respectivement NbEug, NbRang et NbRoul).
        
        Auteur: SCHLEE Adam
    """    
    
    root = Tk()
    root.title("Paramètres de stratégie (Sélection)")
    root.resizable(width=False, height=False)                        # Empêche le redimensionnement de la fenêtre.
    root.configure(bg='MistyRose4', padx=5, pady=5)                  # Donne la couleur de fond de la fenêtre + le padding.
    
    def SetNbEugRangRang():
        global NbEug,NbRang,NbRoul
        NbEug = ceil(NbEugVar.get() * (NbIndividus//2) /100)
        NbRang = round((NbRangRoulVar.get() - NbEugVar.get()) * (NbIndividus//2) /100)
        NbRoul = round((100 - NbRangRoulVar.get()) * (NbIndividus//2) /100)
        root.destroy()

    def ShowHelp():
        HelpWindow  = Toplevel(root)
        HelpWindow.geometry("1010x570+50+10") 
        HelpWindow.resizable(width=False, height=False)              
        HelpWindow.configure(bg='MistyRose4', padx=5, pady=5)
        HelpWindow.title("Aide")
        ImgContainer = Canvas(HelpWindow, width = 1010, height = 530,highlightthickness = 0)
        OkButton = Button(HelpWindow,text="Ok",bg="FireBrick1",command=HelpWindow.destroy, relief="raised", overrelief="sunken")
        HelpImg = PhotoImage(file = "aide.png")
        ImgContainer.create_image(0,0,anchor=NW,image=HelpImg)
        ImgContainer.focus_set()
        ImgContainer.image = HelpImg
        ImgContainer.pack()
        OkButton.pack(side=RIGHT,ipadx=5)


    NbEugVar = IntVar(value = NbEug*100//(NbIndividus//2))
    NbRangRoulVar = IntVar(value = NbRang*100//(NbIndividus//2) + NbEugVar.get())
    NbEugLabel = Label(root,text="Sélection par eugénisme",bg = "MistyRose4",fg="MistyRose1", font=('Helvetica',12))
    NbRangLabel = Label(root,text="Sélection par rang",bg = "MistyRose4",fg="MistyRose1", font=('Helvetica',12))
    NbRoulLabel = Label(root,text="Sélection par roulette",bg = "MistyRose4",fg="MistyRose1", font=('Helvetica',12))
    NbEugRangScale= Scale(root, highlightthickness = 0, bd = 0, bg = "MistyRose4",fg="MistyRose1", troughcolor = "gray25", activebackground = "lightblue", orient='horizontal', sliderrelief="groove", variable=NbEugVar, from_=1, to=27,resolution=1, tickinterval=4, length=200)
    NbRangRoulScale= Scale(root, highlightthickness = 0, bd = 0, bg = "MistyRose4",fg="MistyRose1", troughcolor = "gray25", activebackground = "lightblue", orient='horizontal', sliderrelief="groove", variable=NbRangRoulVar, from_=28, to=100,resolution=1, tickinterval=6, length=400)
    BoutonFrame = Frame(root, bg = "MistyRose4")
    BoutonNext = Button(BoutonFrame, text ="Next", bg="firebrick1", command = SetNbEugRangRang, relief="raised", overrelief="sunken")
    BoutonHelp = Button(BoutonFrame, text ="Aide", bg="orange", command = ShowHelp, relief="raised", overrelief="sunken")
    NbEugLabel.grid(row=0,column=0)
    NbRangLabel.grid(row=0,column=1)
    NbRoulLabel.grid(row=0,column=2)
    NbEugRangScale.grid(row=1,column=0)
    NbRangRoulScale.grid(row=1,column=1, columnspan=2)
    BoutonFrame.grid(row=2, columnspan=3, sticky="e", padx=5, pady=5)
    BoutonHelp.pack(side = LEFT, padx=5, pady=5)
    BoutonNext.pack(side = LEFT, padx=5, pady=5)
    
    root.mainloop()
    
def ModifierParamReprod():
    """
    Spécification :
    
        Entrée: Aucune

        Sortie: Aucune (Modifie les variables globales NbMutation et Nbhybr)

        Rôle:   L'utilisateur choisit le nombre de reproduction(s) par mutation et hybridation (respectivement NbMutation et NbHybridation).
        
        Auteur: SCHLEE Adam
    """ 
    root = Tk()
    root.title("Paramètres de stratégie (Reproduction)")
    root.resizable(width=False, height=False)                        # Empêche le redimensionnement de la fenêtre.
    root.configure(bg='MistyRose4', padx=5, pady=5)                  # Donne la couleur de fond de la fenêtre + le padding.
        
    def SetNbMutHybr():
        global NbMutation,NbHybr
        NbMutation = ceil(NbMutHybrVar.get() * (NbIndividus-NbEug) /100)
        NbHybr = (100 - NbMutHybrVar.get()) * (NbIndividus-NbEug) //100
        root.destroy()

    def ShowHelp():
        HelpWindow  = Toplevel(root)
        HelpWindow.geometry("1010x510+50+10") 
        HelpWindow.resizable(width=False, height=False)              
        HelpWindow.configure(bg='MistyRose4', padx=5, pady=5)
        HelpWindow.title("Aide")
        ImgContainer = Canvas(HelpWindow, width = 1010, height = 470,highlightthickness = 0)
        OkButton = Button(HelpWindow,text="Ok",bg="FireBrick1",command=HelpWindow.destroy, relief="raised", overrelief="sunken")
        HelpImg = PhotoImage(file = "aide2.png")
        ImgContainer.create_image(0,0,anchor=NW,image=HelpImg)
        ImgContainer.focus_set()
        ImgContainer.image = HelpImg
        ImgContainer.pack()
        OkButton.pack(side=RIGHT,ipadx=5)
        
    NbMutHybrVar = IntVar(value = NbMutation*100//(NbIndividus-NbEug))
    NbMutLabel = Label(root,text="Reproduction par mutation",bg = "MistyRose4",fg="MistyRose1", font=('Helvetica',12))
    NbHybrLabel = Label(root,text="Reproduction par hybridation",bg = "MistyRose4",fg="MistyRose1", font=('Helvetica',12))
    NbMutHybrScale= Scale(root, highlightthickness = 0, bd = 0, bg = "MistyRose4",fg="MistyRose1", troughcolor = "gray25", activebackground = "lightblue", orient='horizontal', sliderrelief="groove", variable=NbMutHybrVar, from_=0, to=100,resolution=1, tickinterval=5, length=600)
    BoutonFrame = Frame(root, bg = "MistyRose4")
    BoutonNext = Button(BoutonFrame, text = "Next", bg = "FireBrick1", command = SetNbMutHybr, relief="raised", overrelief="sunken")
    BoutonHelp = Button(BoutonFrame, text ="Aide", bg="orange", command = ShowHelp, relief="raised", overrelief="sunken")
    NbMutLabel.grid(row=0,column=0)
    NbHybrLabel.grid(row=0,column=1)
    NbMutHybrScale.grid(row=1, columnspan=2)
    BoutonFrame.grid(row=2, columnspan=2, sticky="e", padx=5, pady=5)
    BoutonHelp.pack(side = LEFT, padx=5, pady=5)
    BoutonNext.pack(side = LEFT, padx=5, pady=5)
    
    root.mainloop()

def ModifierNbGenMax():
    """
    Spécification :
    
        Entrée: Aucune

        Sortie: Aucune (Modifie la variable globale NbGenMax)

        Rôle:   L'utilisateur choisit le nombre de génération(s) à partir duquel le programme affiche un résultat même si il n'y a pas eu d'amélioration (NbGenMax) 
        
        Auteur: SCHLEE Adam
    """ 
    root = Tk()
    root.title("Paramètres de stratégie")
    root.resizable(width=False, height=False)                        # Empêche le redimensionnement de la fenêtre.
    root.configure(bg='MistyRose4', padx=5, pady=5)                  # Donne la couleur de fond de la fenêtre + le padding.
        
    def SetNbGenMax():
        global NbGenMax
        NbGenMax = NbGenMaxVar.get()
        root.destroy()
        
    NbGenMaxVar = IntVar(value = NbGenMax)
    NbGenLabel = Label(root,text="Nombre de génération(s) à partir duquel le programme affiche un résultat même si il n'y a pas eu d'amélioration :",bg = "MistyRose4",fg="MistyRose1", font=('Helvetica',12))
    NbGenEntry = Entry(root,textvariable=NbGenMaxVar,bg = "MistyRose4",fg="MistyRose1", font=('Helvetica',12))
    BoutonNext = Button(root, text = "Next", bg = "FireBrick1", command = SetNbGenMax, relief="raised", overrelief="sunken")
    NbGenLabel.grid(row=0,column=0)
    NbGenEntry.grid(row=0,column=1)
    BoutonNext.grid(row=2, columnspan=2, sticky="e", padx=5, pady=5)
    
    root.mainloop()

def ConfirmerParam():
    """
    Spécification :
    
        Entrée: Aucune

        Sortie: Aucune 

        Rôle:   Affiche les paramètres de stratégie qu'a choisis l'utilisateur. 
                Il a aussi la possibilité de les changer si ces derniers ne lui plaisent pas.
        
        Auteur: SCHLEE Adam
    """ 
    root = Tk()
    root.title("Paramètres de stratégie")
    root.resizable(width=False, height=False)                        # Empêche le redimensionnement de la fenêtre.
    root.configure(bg='MistyRose4')                                  # Donne la couleur de fond de la fenêtre.
   
    def Remodifier():
        
        root.destroy()
        AncienNbIndividus = NbIndividus
        if NbGeneration == 0:
            ModifierNbIndividu()
        global NbEug, NbRang, NbRoul, NbMutation, NbHybr
        AncienNbEug = NbEug
        NbEug = ceil((NbEug/(AncienNbIndividus//2)) * ceil(NbIndividus/2))       
        NbRang = ceil(NbRang/(AncienNbIndividus//2) * ceil(NbIndividus/2))         
        NbRoul = ceil(NbIndividus/2) - NbEug - NbRang                     
        ModifierParamSelection()
        NbMutation = ceil((NbMutation/(AncienNbIndividus-AncienNbEug)) * (NbIndividus-NbEug))             
        NbHybr = NbIndividus - NbMutation - NbEug    
        ModifierParamReprod()
        ModifierNbGenMax()
        ConfirmerParam()
        
    SuccesLabel = Label(root, text = 'Les paramètres de stratégie ont été confirmés',bg = "MistyRose4",fg="MistyRose1", font=('Helvetica',15, 'bold'))
    NbIndLabel = Label(root,text="Nombre d'individus : " + str(NbIndividus),bg = "MistyRose4",fg="MistyRose1", font=("Helvetica",12))    
    SelecFrame = LabelFrame(root,text = "Sélection",bg = "MistyRose4",fg="MistyRose1")
    ReprodFrame = LabelFrame(root,text = "Reproduction",bg = "MistyRose4",fg="MistyRose1")
    NbEugLabel = Label(SelecFrame,text="Sélection par eugénisme : " + str(NbEug),bg = "MistyRose4",fg="MistyRose1", font=("Helvetica",12))
    NbRangLabel = Label(SelecFrame,text="Sélection par rang : " + str(NbRang),bg = "MistyRose4",fg="MistyRose1", font=("Helvetica",12))
    NbRoulLabel = Label(SelecFrame,text="Sélection par roulette : " + str(NbRoul),bg = "MistyRose4",fg="MistyRose1", font=("Helvetica",12))
    NbMutLabel = Label(ReprodFrame,text="Reproduction par mutation : " + str(NbMutation),bg = "MistyRose4",fg="MistyRose1", font=("Helvetica",12))
    NbHybrLabel = Label(ReprodFrame,text="Reproduction par hybridation : " + str(NbHybr),bg = "MistyRose4",fg="MistyRose1", font=("Helvetica",12))
    BoutonChange = Button(root, text ="Modifier", bg="lightblue", command = Remodifier, relief="raised", overrelief="sunken")
    BoutonNext = Button(root, text ="Ok", bg="FireBrick1", command = root.destroy, relief="raised", overrelief="sunken")
    
    SuccesLabel.pack(padx=10,pady=10)
    NbIndLabel.pack(anchor='w',padx = 10)
    SelecFrame.pack(fill=X, side=TOP,padx=10,pady=10)
    ReprodFrame.pack(fill=X, side=TOP,padx=10,pady=10)
    NbEugLabel.pack(anchor='w')
    NbRangLabel.pack(anchor='w')
    NbRoulLabel.pack(anchor='w')
    NbMutLabel.pack(anchor='w')
    NbHybrLabel.pack(anchor='w')
    BoutonNext.pack(side = RIGHT, padx=5, pady=5)
    BoutonChange.pack(side = RIGHT, padx=5, pady=5)
    
    root.mainloop()

def Eden(Villes):
    """
    Spécification :

    Entrée: Dictionnaire de villes
    Ex :{ '1': (x,y), '2': (x,y), '3': (x,y),'4': (x,y), '5': (x,y), '6': (x,y) }
    Avec x et y les coordonnées de la ville et '1','2','3',... le nom des villes.

    Sortie: Population (liste)
    Ex : [ [ ['1','2','3','4'],inf],
           [ ['1','3','2','4'],inf],
           [ ['1','3','4','2'],inf] ]

    Role: Le programme génère une population aléatoire à partir du dictionnaire de villes

    Auteur: FAHEM Rayene
    """

    Cities = [key for key in Villes]
    FirstCities = Cities.pop(0)
    Population = [[random.sample(Cities, len(Cities)), inf] for i in range(NbIndividus)]
    for i in range(NbIndividus):
        Population[i][0].insert(0,FirstCities)

    return Population

def Evaluer(Villes,Population):
    """
    Spécification :
    
        Entrée: Population (liste)
                Ex :  [ [ ['1','2','3','4'],inf ],
                        [ ['1','3','2','4'],inf ],
                        [ ['1','3','4','2'],inf ] ]

        Sortie: PopulationEval (liste)
                Ex : [ [ ['1','2','3','4'], 7 ],
                       [ ['1','3','2','4'], 6 ],
                       [ ['1','3','4','2'], 1 ] ]

        Rôle:   Le programme évalue les chemins en calculant la distance parcourue avec chacun puis l'ajoute dans la liste PopulationEval,
                de manière à ce que : PopulationEval[i][0] = chemin n°i, PopulationEval[i][1] = distance parcourue avec le chemin n°i (performance)
        
        Auteur: GEOFFROY Alexandre
    """
    PopulationEval = []                                # Création de la liste de sortie.
    for Individu in Population:                        # Pour chaque chemin (liste de villes) de la liste totale des chemins.
        distance = 0        
        for ville in range(1,len(Individu[0])):        # Pour chaque ville du chemin en partant de la deuxième.
            Ville1 = Villes[Individu[0][ville-1]]      # Ville précédente de la liste.
            Ville2 = Villes[Individu[0][ville]]        # Ville de la liste.
            # Coordonnées de chaque ville.
            x1, y1, x2, y2 = Ville1[0], Ville1[1], Ville2[0], Ville2[1]
            # Distance entre chaque ville calculée grâce au théorème de Pythagore.
            distance += sqrt(((x2-x1)**2) + ((y2-y1)**2))
        Individu[1] = distance                         # On remplace le inf (deuxième valeur de la liste des chemins) par la distance qu'on vient de calculer.
        PopulationEval.append(Individu)                # Remplissage de la liste de sortie avec le chemin actuel (avec la distance parcourue au lieu de inf).
    return PopulationEval

def Trier(PopulationEval,Score):
    """
    Spécification :
    
        Entrée: PopulationEval (liste)
                Ex : [ [ ['1','2','3','4'], 7 ],
                       [ ['1','3','2','4'], 6 ],
                       [ ['1','3','4','2'], 1 ] ]

        Sortie: PopulationTri (liste) , Best (bool) , score (int)
                Ex : [ [ ['1','2','3','4'], 1 ],
                       [ ['1','3','2','4'], 6 ],
                       [ ['1','3','4','2'], 7 ] ]

        Rôle:   Le programme trie la population évaluée (PopulationEval) en fonction de la distance des chemins (du plus petit au plus grand).
        
        Auteur: TORES CORTEZ Shéridan
    """
    global Best

    for i in range(len(PopulationEval)):                        # Pour chaque chemin de la liste
                                                                
        min = i                                                 
        for j in range(i+1,(len(PopulationEval))):              
                                                                
            if PopulationEval[min][1] > PopulationEval[j][1]:   # On compare la performance du chemin n°i avec toutes les autres
                min = j                                         # Si l'une d'elle est plus petite que celle du chemin n°i, alors le chemin n°j prend la place du chemin n°i
                                                                
        tmp = PopulationEval[i]                                 
        PopulationEval[i] = PopulationEval[min]                 
        PopulationEval[min] = tmp                               

    PopulationTri = PopulationEval                              # Changement du nom de la variable par soucis de clarté.
    
    tmpScore = PopulationTri[0][1]                              # Récupération du score du meilleur individu.
    ScoreListe.append(tmpScore)                                 # Ajout de ce score au tableau ScoreListe nécessaire au graphique.

    if tmpScore < Score or Score == inf:                        # Si le score (performance) de cette génération est meilleur que les dernières générations,
        
        Score = tmpScore
        Best = True                                             # La variable globale Best indiquera qu'il y a eu une amélioration
    

    
    return PopulationTri,Best,Score

def Diviser(PopulationTri):
    """
    Spécification :

        Entrée: PopulationTri = liste 
                ex: PopulationTri = [ [ ['1','3','2','4'],2],
                                      [ ['1','4','2','3'],4],
                                      [ ['1','2','4','3'],5],
                                      [ ['1','4','3','2'],8] ]
 
        Sortie: Populationtri = liste 
                ex: PopulationTri = [ [ ['1','3','2','4'],2],
                                      [ ['1','4','2','3'],4], ]

        Rôle: Supprime la moitié la moins performante de la population triée.

        Auteur: SCHLEE Adam
    """
    return PopulationTri[0:ceil(len(PopulationTri)/2)]
    
def SelectionnerParEugenisme(PopulationTri):
    """
    Spécification :

        Entrée: PopulationTri (liste)
                ex: [ [ ['1','2','3','4'], 1 ],
                      [ ['1','3','2','4'], 6 ],
                      [ ['1','3','4','2'], 7 ] ]
 
        Sortie: ListeEug (liste)
                ex: [ [ ['1','3','4','2'], 1 ] ]
                
        Rôle: Retourne une liste de n listes (individus/chemins) les plus performantes (distance la plus courte) 
              avec n le nombre d'individus sélectionnés (NbEug).
        
        Auteure: SIEBERING Juliette
    """
    NewIndividus = []
    
    for i in range(NbEug):
        NewIndividus.append(PopulationTri[i])
        
    return NewIndividus

def SelectionnerParRang(PopulationTri):
    """
    Spécification :

        Entrée: PopulationTri(Liste)
                ex: [ [ ['1','2','3','4'], 2 ],
                      [ ['1','3','2','4'], 4 ],
                      [ ['1','3','4','2'], 7 ] ]
 
        Sortie: ListeRang(Liste)
                ex: [ [ ['1','3','4','2'], 7 ],
                      [ ['1','2','3','4'], 2 ], 
                      [ ['1','3','4','2'], 7 ] ]

        Rôle:  Retourne une liste de n listes (individus/chemins) choisis aléatoirement 
               dans la population triée (PopulationTri) grâce à la méthode de sélection par rang avec n le nombre d'individus
               sélectionnés (NbRang).
        
        Auteur: REZKI Saber
    """

    NbIndividus = len(PopulationTri)

    def SommeDesRangs():
        '''
            Permet de faire la somme des rangs.
            T =  1 + 2 + 3 + ... + NbINdividus
        '''
        Somme = 0
        for NrInd in range(1,NbIndividus+1):
            Somme += NrInd
        return Somme

    Somme = SommeDesRangs()

    ListeRang=[]
    ListeAlea=[]

    def SelecRang(Somme,PopulationTri):
        '''
            Permet de choisir un rang aléatoirement, de prendre la liste correspondant au rang choisi et d'ajouter cette liste
            dans la liste transitoire (ListeRang).
        '''
        DejaFait = True
        while DejaFait:
            RangAlea = random.randint(1,Somme-1)
            Rang = round(RangAlea/Somme*NbIndividus)
            if Rang == NbIndividus: Rang-=1
            if Rang not in ListeAlea:
                ListeAlea.append(Rang)
                DejaFait = False

        Individu = PopulationTri[Rang]
        ListeRang.append(Individu)

    for _ in range(NbRang):
        SelecRang(Somme,PopulationTri)

    return ListeRang

def SelectionnerParRoulette(PopulationTri):
    """
    Spécification :

        Entrée: PopulationTri(Liste)
                ex: [ [ ['1','2','3','4'], 2 ],
                      [ ['1','3','2','4'], 4 ],
                      [ ['1','3','4','2'], 7 ] ]
 
        Sortie: ListeRoul(Liste)
                ex: [ [ ['1','3','4','2'], 4 ],
                      [ ['1','2','3','4'], 2 ], 
                      [ ['1','3','4','2'], 7 ] ]

        Rôle:  Retourne une liste de n listes (individus/chemins) choisis aléatoirement
        dans la population triée (PopulationTri) grâce à la méthode de sélection par roulette avec n le nombre d'individus
        sélectionnés (NbRoul).
        
        Auteures: AZIZ Maissa et SIEBERING Juliette
    """
    NewIndividu = []
    NbRepetition = 0

    for _ in range(NbRoul):
        
        DejaFait = True
        Somme = 0
        for i in range(len(PopulationTri)):
            Somme = Somme + PopulationTri[i][1]
        Max = Somme

        while DejaFait:
            NbRepetition+=1
            Choix = random.uniform(0, Max)
            Current = 0
            for i in range (len(PopulationTri)):
                Current += PopulationTri[i][1]
                if Current > Choix:
                    if PopulationTri[i] not in ListeRang and PopulationTri[i] not in NewIndividu or NbRepetition < 50:
                        NewIndividu.append(PopulationTri[i])
                        DejaFait = False
                        break
                
    return NewIndividu

def SelectionnerParEugenisme2(ListeEug):
    """
    Spécification :

        Entrée: ListeEug 
                ex: [ [ ['1','2','3','4'], 2 ],
                      [ ['1','3','2','4'], 4 ],
                      [ ['1','3','4','2'], 7 ] ]
 
        Sortie: NewIndividus = liste 
                ex: [ [ ['1','3','4','2'],inf],
                      [ ['1','2','3','4'],inf], 
                      [ ['1','3','4','2'],inf] ]
                remarque: la performance des individus (= distance des chemins) sera calculée plus tard, lors de l'évaluation.

        Rôle:  Retourne ListeEug avec les performances (distances) = inf.
               
        Auteur: SCHLEE Adam
    """
    
    NewIndividus = []

    for i in range(NbEug):
    
        NewIndividus.append([ListeEug[i][0],inf])
        
    return NewIndividus

def Muter(ListeEug,ListeRang,ListeRoul):
    """
    Spécification :

        Entrée: ListeEug,ListeRang,ListeRoul = liste 
                ex: [ [ ['1','2','3','4'], 2 ],
                      [ ['1','3','2','4'], 4 ],
                      [ ['1','3','4','2'], 7 ] ]
 
        Sortie: NewIndividus = liste 
                ex: [ [ ['1','3','4','2'],inf],
                      [ ['1','2','3','4'],inf], 
                      [ ['1','3','4','2'],inf] ]
                remarque: la performance des individus (= distance des chemins) sera calculée plus tard, lors de l'évaluation.

        Rôle: Concatène les 3 listes d'entrée en une liste appelée : PopulationTrans
              Crée un nouvel individu "fils" à partir des gènes (villes) d'un individu "père" choisi aléatoirement parmi
              la liste PopulationTrans en intervertissant 2 gènes entre eux.
              Le fils sera alors idendique au père à l'exception de deux gènes qui seront intervertis entre eux.
              ex: Père = ['1','2','3','4'] -> Fils = ['1','3','2','4']
              Cette fonction sera répétée autant de fois que l'indique le nombre NbMutation.

        Auteur: SCHLEE Adam
    """
    PopulationTrans = []

    for i in range(len(ListeEug)):
        PopulationTrans.append(ListeEug[i])
        
    for i in range(len(ListeRang)):
        PopulationTrans.append(ListeRang[i])
        
    for i in range(len(ListeRoul)):
        PopulationTrans.append(ListeRoul[i])

    NbVilles = len(PopulationTrans[0][0])
    NewIndividus = []
    ValeurAleatoire = []
    
    for _ in range(NbMutation):
        
        DejaFait = True
        
        while DejaFait:                                    # On vérifie qu'il n'y ait pas 2 fois la même mutation.

            i,j,k = random.randint(1,NbVilles-2),random.randint(1,NbVilles-2),random.randint(0,len(PopulationTrans)-1)
            
            if (i,j,k) not in ValeurAleatoire:
                
                DejaFait = False
                
        ValeurAleatoire.append((i,j,k))

        Pere = deepcopy(PopulationTrans[k])                 # Le module deepcopy permet de faire une copie de la liste "PopulationTrans[k]",
        Fils = deepcopy(PopulationTrans[k])                 # afin qu'uniquement la variable "père" soit modifiée et non la "PopulationTrans[k]"
        
        Fils[0][j] = Pere[0][i+1]                           # Principe de mutation
        Fils[0][i+1] = Pere[0][j]                           # -
        Fils[1] = inf
        
        NewIndividus.append(Fils)
        
    return NewIndividus

def Hybrider(ListeEug,ListeRang,ListeRoul):
    """
    Spécification :

        Entrée: ListeEug,ListeRang,ListeRoul
                ex:
                ListeEug  = [ [ ['1','2','3','4'],2] ]

                ListeRang = [ [ ['1','3','2','4'],4],
                              [ ['1','2','3','4'],9],
                              [ ['1','2','4','3'],5] ]

                ListeRoul = [ [ ['1','3','2','4'],4],
                              [ ['1','2','3','4'],7],
                              [ ['1','2','4','3'],5] ]

                
        Sortie: NewIndividus = liste 
                ex: [ [ ['1','3','4','2'],inf],
                      [ ['1','2','3','4'],inf], 
                      [ ['1','3','4','2'],inf] ]
                remarque: la performance des individus (=distance des chemins) sera calculé après lors de l'évaluation.

        Role:Choisie une liste au hasard dans la liste eugénisme(Liste Eug) et une liste au hasard de Roulette/Rang. prends la moitié des valeur de la liste eugénisme de manière aléatoire pour les remplacer dans liste Roulette/Rang  
        Ex: liste eugenisme = ['1','2','3','4'],2] + liste Roulette =[['1','3','2','4'],4] -> liste finale = ['1','2','4','3']

        Auteur: ACIKBAS Tuna
    """
    
    NewIndividus = []
    NbTour = 0
  

    for _ in range(NbHybr):

        NewindividusTest = []
        ListeSelec = []
        AleaVilleEug = []
        AleaVilleSelec =[]
        NewChemin = []

        # Mettre ListeRang et ListeRoul dans une même liste (ListeSelec).
        for i in range(len(ListeRang)):
            ListeSelec.append(ListeRang[i])
        for i in range(len(ListeRoul)):
            ListeSelec.append(ListeRoul[i])

        if len(ListeEug) > 1:
            ListeAleatoireEugenisme = random.randint(0,(len(ListeEug)-1)) 
        else:
            ListeAleatoireEugenisme = 0
            
        ListeAleatoireListeSelec = random.randint(0,(len(ListeSelec)-1))
        
        # Prendre un individu aléatoire de ListeEug et l'enregistrer dans la variable AleaListeEug. Ne prendre que le chemin, pas la distance
        AleaListeEug = ListeEug[ListeAleatoireEugenisme][0]

        # Prendre un individu aléatoire de ListeSelec et l'enregistrer dans la variable AleaListeSelec. Ne prendre que le chemin, pas la distance
        AleaListeSelec = ListeSelec[ListeAleatoireListeSelec][0]

        # Prendre ceil(n/2) villes de AleaListeEug (avec len(AleaListeEug[0]) == n) qui seront enregistré dans la variable AleaVilleEug (list) 
        # en vérifiant que les éléments pris ne sont pas dans la premiere moitié de AleaListeSelec.
        TailleAleaListeEug = len(AleaListeEug)
        Limite = floor(TailleAleaListeEug/2)
        
        while len(AleaVilleEug) != Limite:

            VilleAjouter = AleaListeEug[random.randint(1,len(AleaListeEug)-1)]
            if VilleAjouter in AleaListeSelec[:Limite] or VilleAjouter in AleaVilleEug:
                VilleAjouter = AleaListeEug[random.randint(1,len(AleaListeEug)-1)]
            else:
                AleaVilleEug.append(VilleAjouter)
    
        # On prend ceil(n/2) villes de la AleaListeSelec (avec len(AleaListeSelec[0]) == n) qui seront enregistré dans la variable AleaVilleSelec (list).
        # en vérifiant que les éléments pris ne sont pas dans la premiere moitié de AleaListeEug.
        while len(AleaVilleSelec) != Limite:
            VilleAjouter = AleaListeSelec[random.randint(1,len(AleaListeSelec)-1)]
            if VilleAjouter in AleaListeEug[:Limite] or VilleAjouter in AleaVilleSelec:
                VilleAjouter = AleaListeSelec[random.randint(1,len(AleaListeSelec)-1)]
            else:
                AleaVilleSelec.append(VilleAjouter)
        
        # On prend un nombre aléatoire entre 0 et 1, si c'est 0, on fait ind12 (voir doc prof) sinon on fait ind21.
        NombreAlea = random.randint(0,1)

        # Pour ind12 : On prend la premiere moitié de la AleaListeEug et on l'ajoute dans une variable NewChemin
        # Ensuite, on ajoute dans NewIndividu les éléments de AleaVilleSelec
        if NombreAlea ==0:
            AleaListeEug = AleaListeEug[:Limite]
            for i in range(Limite):
                NewChemin.append(AleaListeEug[i])
            for i in range(Limite):
                NewChemin.append(AleaVilleSelec[i])

        # Pour ind21 : On prend la premiere moitié de la AleaListeSelec et on l'ajoute dans une variable NewChemin
        elif NombreAlea ==1:
            AleaListeSelec = AleaListeSelec[:Limite]
            for i in range(Limite):
                NewChemin.append(AleaListeSelec[i])
                
            for i in range(Limite):
                NewChemin.append(AleaVilleEug[i])

                    # Ensuite, on ajoute dans NewIndividu les éléments de AleaVilleEug
        # Enfin, on ajoute NewIndividu dans la liste NewIndividus en lui ajoutant inf en distance (NewIndividus.append([NewIndividu,inf]))
   
        NewindividusTest.append([NewChemin,inf])
        if NewindividusTest not in NewIndividus or NbTour > 50:
            NbTour = 0
            NewIndividus.append([NewChemin,inf])
        else:
            NbTour += 1
            Hybrider(ListeEug,ListeRang,ListeRoul)
        # Et on recommence NbHybr fois
        

        # Une fois qu'on a fais ce qui est au dessus NHybr fois, on retourne la liste NewIndividus.
    
    return NewIndividus

def Concatener(ListeEug2,ListeMut,ListeHybr):
    """
    Spécification :

        Entrée: ListeEug2,ListeMutg,ListeHybr = liste 
                ex: ListeEug2 = [ [ ['1','2','3','4'],inf] ]

                    ListeMut  = [ [ ['1','3','2','4'],inf],
                                  [ ['1','2','3','4'],inf],
                                  [ ['1','2','3','4'],inf] ]

                    ListeHybr = [ [ ['1','3','2','4'],inf],
                                  [ ['1','4','2','3'],inf],
                                  [ ['1','2','4','3'],inf] ]
 
        Sortie: NewPopulation = liste 
                ex: NewPopulation = [ [ ['1','2','3','4'],inf],
                                      [ ['1','3','2','4'],inf],
                                      [ ['1','2','3','4'],inf],
                                      [ ['1','2','3','4'],inf],
                                      [ ['1','3','2','4'],inf],
                                      [ ['1','4','2','3'],inf],
                                      [ ['1','2','4','3'],inf] ]

                Remarque: la performance des individus (= distance des chemins) sera calculée plus tard, lors de l'évaluation.

        Rôle: Concatène les 3 listes d'entrée en une liste appelée : NewPopulation
              Autrement dit : Crée la nouvelle population (la génération suivante)

        Auteur: SCHLEE Adam
    """
    NewPopulation = []

    for i in range(len(ListeEug2)):
        NewPopulation.append(ListeEug2[i])
        
    for i in range(len(ListeMut)):
        NewPopulation.append(ListeMut[i])
        
    for i in range(len(ListeHybr)):
        NewPopulation.append(ListeHybr[i])

    return NewPopulation

def AfficherResultat(Villes,MeilleurIndividu,Score):
    """
    Spécification :

        Entrée: Villes = Dict, MeilleurIndividu = list 
                ex: Villes = {'1':(12,89),'2':(63,49),'3':(29,78),'4':(91,34),'5':(12,13),'6':(76,78)}

                    MeilleurIndividu  = [ ['1','2','3','6','5'],2 ]
                                  
        Sortie: Modification de la variable globale : Continue (bool),
        
                Carte avec le chemin correspondant au meilleur individu de la n-ième génération.

        Rôle: Affiche le chemin correspondant au meilleur individu de la n-ième génération sur la carte.

        Auteur: SCHLEE Adam
    """
    root = Tk()
    root.geometry("600x450+50+10")
    root.title("Résultat")
    root.configure(bg='MistyRose4')                                  # Donne la couleur de fond de la fenêtre.
    root.resizable(width=False, height=False)                        # Empêche le redimensionnement de la fenêtre.
    photo=PhotoImage(file="carte.png")
    canvas = Canvas(root,width=550, height=382)
    canvas.create_image(0, 0, anchor=NW, image=photo)
    
    label = Label(root, text="")
    label.config(bg='MistyRose4')
    label.pack()
    r = 5
    
    def next():
        global Continue
        Continue = True
        root.destroy()
    
    def exit():
        global Continue
        Continue = False
        root.destroy()

    def Graph():
        X = []
        Y = []
        for i in range (len(ScoreListe)):
            X.append(ScoreListe[i])
        for i in range(len(NbGenerationTotalListe)):
            Y.append(NbGenerationTotalListe[i])

        plt.plot(Y,X,c ="r")
        plt.xlabel("NbGeneration")
        plt.xscale("log")
        plt.ylabel("Distance")
        plt.show()

    def Modif():

        root.destroy()
        
        ModifierParamSelection()

        ModifierParamReprod()

        ModifierNbGenMax()

        ConfirmerParam()

    
    for i in range(len(MeilleurIndividu[0])-1):
        Individu1 = MeilleurIndividu[0][i]
        Individu2 = MeilleurIndividu[0][i+1]
        canvas.create_rectangle((Villes[Individu1][0])-r, Villes[Individu1][1]-r, Villes[Individu1][0]+r,Villes[Individu1][1]+r, outline='black',fill='gray')
        canvas.create_line(Villes[Individu1][0],Villes[Individu1][1],Villes[Individu2][0],Villes[Individu2][1], width= 5, fill="red")
        canvas.create_rectangle((Villes[Individu2][0])-r, Villes[Individu2][1]-r, Villes[Individu2][0]+r,Villes[Individu2][1]+r, outline='black',fill='gray')

    label.pack()
    canvas.focus_set()
    canvas.pack()
    
    BoutonNext  = Button(root, text="Next", command= next, bg="lightblue", relief="raised", overrelief="sunken")
    BoutonNext.pack(side= RIGHT, padx=5, pady=5)
    
    BoutonGraph  = Button(root, text="Graph", command= Graph, bg="orange", relief="raised", overrelief="sunken")
    BoutonGraph.pack(side= RIGHT, padx=5, pady=5)

    BoutonExit  = Button(root, text="Exit", command= exit, bg="FireBrick1", relief="raised", overrelief="sunken")
    BoutonExit.pack(side= RIGHT, padx=5, pady=5)
    
    BoutonModif  = Button(root, text="Modif", command= Modif, bg="lightgreen", relief="raised", overrelief="sunken")
    BoutonModif.pack(side= RIGHT, padx=5, pady=5)

    PerfString = StringVar()
    Perflabel = Label(root, textvariable=PerfString, bg = "MistyRose4",fg="MistyRose1", font=("Helvetica",10) )
    PerfString.set("Distance: " + str(int(Score)))
    Perflabel.pack(side= LEFT, padx=5, pady=5)


    GenString = StringVar()
    Genlabel = Label(root, textvariable=GenString,bg = "MistyRose4",fg="MistyRose1", font=("Helvetica",10) )
    GenString.set("Génération : " + str(NbGenerationTotal))
    Genlabel.pack(side= LEFT, padx=5, pady=5)

    UpgrString = StringVar()
    Upgrlabel = Label(root, textvariable=UpgrString,bg = "MistyRose4",fg="MistyRose1", font=("Helvetica",10) )
    UpgrString.set("Amélioration : " + str(Best))

    Upgrlabel.pack(side= LEFT, padx=5, pady=5)

    root.protocol("WM_DELETE_WINDOW",sys.exit)

    root.mainloop()

#------------------------------------------------------------------------------------------------#

#--------------------------------------STRUCTURE DU PROGRAMME------------------------------------#

Villes = AfficherInterface()

NbIndividus = len(DicoVilles)                   

ModifierNbIndividu()

NbEug = ceil(0.1 * ceil(NbIndividus/2))         
NbRang = ceil(0.6 * ceil(NbIndividus/2))        
NbRoul = ceil(NbIndividus/2) - NbEug - NbRang   

ModifierParamSelection()

NbMutation = ceil((NbIndividus-NbEug)/2)        
NbHybr = floor((NbIndividus-NbEug)/2)           

ModifierParamReprod()

ModifierNbGenMax()

ConfirmerParam()

Population = Eden(Villes) # Eden

while Continue:
       
    while Best == False and NbGeneration <= NbGenMax:
        
        PopulationEval = Evaluer(Villes, Population) # Evaluation
         
        PopulationTri,Best,Score = Trier(PopulationEval,Score) # Tri
        
        PopulationTri = Diviser(PopulationTri)

        # ------------------ Séléction ------------------

        ListeEug = SelectionnerParEugenisme(PopulationTri)

        ListeRang = SelectionnerParRang(PopulationTri)
            
        ListeRoul = SelectionnerParRoulette(PopulationTri)
        
        # -----------------------------------------------

        # ---------------- Reproduction -----------------

        ListeEug2 = SelectionnerParEugenisme2(ListeEug)
        
        ListeMut = Muter(ListeEug,ListeRang,ListeRoul)
         
        ListeHybr = Hybrider(ListeEug,ListeRang,ListeRoul)
        
        # -----------------------------------------------
        
        Population = Concatener(ListeEug2,ListeMut,ListeHybr)

        NbGeneration +=1
        NbGenerationTotal +=1
        NbGenerationTotalListe.append(NbGenerationTotal)
        MeilleurIndividu = ListeEug[0]

    
    AfficherResultat(Villes,MeilleurIndividu,Score)

    NbGeneration,Best = 0,False

#------------------------------------------------------------------------------------------------#
