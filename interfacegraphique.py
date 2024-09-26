#9
import time
import sys 
import os

from tkinter import *
from functools import partial
from random import randint

def remplissage_tableau(x,y,T):
    for y in range(y):
        T.append([])
        for _ in range(x):
            T[y].append(0)

def Int_jeu(x,y,difficulte):
    if difficulte == 1: nombres_mines = int(x*y*0.125)
    elif difficulte == 2: nombres_mines = int(x*y*(1000/6300))
    elif difficulte == 3: nombres_mines = int(x*y*0.20625)
    T=[]
    remplissage_tableau(x,y,T)
    mines_placees = 0
    while nombres_mines != mines_placees:
        x_mine = randint(0,x-1)
        y_mine = randint(0,y-1)
        if T[y_mine][x_mine] != 2:
            T[y_mine][x_mine] = 2
            mines_placees += 1
    return T,nombres_mines

def mines_autour(T):
    matriceT = []
    remplissage_tableau(len(T[0]),len(T),matriceT)
    for y in range(len(T)):
        for x in range(len(T[0])):
            mines_proximite = 0
            if y != 0 and x != 0:
                if T[y-1][x-1] == 2:    mines_proximite += 1
            if y != 0:
                if T[y-1][x] == 2:      mines_proximite += 1
            if y != 0 and x != len(T[0])-1:
                if T[y-1][x+1] == 2:    mines_proximite += 1
            if x != 0:
                if T[y][x-1] == 2:      mines_proximite += 1
            if x != len(T[0])-1:
                if T[y][x+1] == 2:      mines_proximite += 1
            if y != len(T)-1 and x != 0:
                if T[y+1][x-1] == 2:    mines_proximite += 1
            if y != len(T)-1 :
                if T[y+1][x] == 2:      mines_proximite += 1
            if y != len(T)-1 and x != len(T[0])-1:
                if T[y+1][x+1] == 2:    mines_proximite += 1
            matriceT[y][x] = mines_proximite
    return matriceT

def poser_drapeau(T,x,y):
    if T[y][x] == 0: T[y][x] = 3
    elif T[y][x] == 2: T[y][x] = 4

def lever_drapeau(T,x,y):
    if T[y][x] == 3:
        T[y][x] = 0
    elif T[y][x] == 4:
        T[y][x] = 2

def creuser(T,matriceT,x,y):
    global N, tableau, listeImage                #j'ai mis cela parce que sinon, la variable N revient toujours à 0 bizarement
    if T[y][x] == 0:
        T[y][x] = 1
        N += 1
        tableau.delete(listeImage[y][x])
        affichageSingulier(x, y)
        return True
    elif T[y][x] == 2: return False

def creuser_recu(T,matriceT,x,y):
    global N, tableau, listeImage
    if matriceT[y][x] == 0 and T[y][x] == 0:
        T[y][x] = 1
        N += 1
        tableau.delete(listeImage[y][x])
        affichageSingulier(x, y) 
        if x != 0 and y != 0: creuser_recu(T,matriceT,x-1,y-1)
        if y != 0: creuser_recu(T,matriceT,x,y-1)
        if x != len(T[0])-1 and y != 0: creuser_recu(T,matriceT,x+1,y-1)
        if x != 0: creuser_recu(T,matriceT,x-1,y)
        if x != len(T[0])-1: creuser_recu(T,matriceT,x+1,y)
        if x != 0 and y != len(T)-1: creuser_recu(T,matriceT,x-1,y+1)
        if y != len(T)-1: creuser_recu(T,matriceT,x,y+1)
        if x != len(T[0])-1 and y != len(T)-1: creuser_recu(T,matriceT,x+1,y+1)
        return True
    else:    
        return creuser(T,matriceT,x,y)


def timer():
    global debutTimer, Terminer, minute, seconde
    finTimer = time.time()
    TempsPris = int(finTimer - debutTimer)
    minute = TempsPris//60
    seconde = TempsPris%60
    if seconde<10: texteTimer = str(minute)+":"+("0"+str(seconde))
    else: texteTimer = str(minute)+":"+str(seconde)
    labelTimer.configure(text=texteTimer)
    if Terminer == False: timerAfter = labelTimer.after(200,timer)

def score():
    global debutTimer, N, Terminer, textScore
    finTimer = time.time()
    TempsPris = int(finTimer - debutTimer)
    pointsEnleves = TempsPris//10
    textScore = str(int(N*500)-(int(pointsEnleves)*4000))
    textScoreLabel = "Score : " + textScore
    labelScore.configure(text=textScoreLabel)
    if Terminer == False: scoreAfter = labelScore.after(100,score)


def SetDiff(diff):
    global difficulte
    if diff == 1:
        difficulte = 1
        sliderLongueur.set(10)
        sliderHauteur.set(8)
    elif diff == 2:
        difficulte = 2
        sliderLongueur.set(18)
        sliderHauteur.set(14)
    elif diff == 3:
        difficulte = 3
        sliderLongueur.set(24)
        sliderHauteur.set(20)

def ValeurGet():
    global longueur, hauteur
    longueur = sliderLongueur.get()
    hauteur = sliderHauteur.get()

# from https://stackoverflow.com/questions/31836104/pyinstaller-and-onefile-how-to-include-an-image-in-the-exe-file
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def creationImage():
    global imageBombe, imageDrapeau, imageDrapeauMS, imageCase, imageCreusee, imageMineCreusee, image1, image2, image3, image4, image5, image6, image7, image8
    imageBombe = PhotoImage(file=resource_path("images/case/mine.png"))            #création des images des cases
    imageDrapeau = PhotoImage(file=resource_path("images/case/drapeau.png"))
    imageDrapeauMS = PhotoImage(file=resource_path("images/case/drapeauMisplace.png"))
    imageCase = PhotoImage(file=resource_path("images/case/case.png"))
    imageCreusee = PhotoImage(file=resource_path("images/case/casecreuse.png"))
    imageMineCreusee = PhotoImage(file=resource_path("images/case/minecreusee.png"))

    image1 = PhotoImage(file=resource_path("images/chiffres/1.png"))               #images pour les cases creusées
    image2 = PhotoImage(file=resource_path("images/chiffres/2.png"))
    image3 = PhotoImage(file=resource_path("images/chiffres/3.png"))
    image4 = PhotoImage(file=resource_path("images/chiffres/4.png"))
    image5 = PhotoImage(file=resource_path("images/chiffres/5.png"))
    image6 = PhotoImage(file=resource_path("images/chiffres/6.png"))
    image7 = PhotoImage(file=resource_path("images/chiffres/7.png"))
    image8 = PhotoImage(file=resource_path("images/chiffres/8.png"))

def affichageGraphique():
    global listeImage, tailleCase
    listeImage = []                                     #cette liste va nous permettre de selctionner une certaine image sur le terrain
    remplissage_tableau(longueur,hauteur,listeImage)
    for y in range (hauteur):
        for x in range (longueur):
            if T[y][x] == 0: 
                case = tableau.create_image((x*tailleCase)+2, (y*tailleCase)+2, anchor=NW, image=imageCase)
                listeImage[y][x] = case
            elif T[y][x] == 1 :
                if matriceT[y][x] == 0 : 
                    case = tableau.create_image((x*tailleCase)+2, (y*tailleCase)+2, anchor=NW, image=imageCreusee)
                    listeImage[y][x] = case
                elif matriceT[y][x] == 1 : 
                    case = tableau.create_image((x*tailleCase)+2, (y*tailleCase)+2, anchor=NW, image=image1)
                    listeImage[y][x] = case
                elif matriceT[y][x] == 2 : 
                    case = tableau.create_image((x*tailleCase)+2, (y*tailleCase)+2, anchor=NW, image=image2)
                    listeImage[y][x] = case
                elif matriceT[y][x] == 3 : 
                    case = tableau.create_image((x*tailleCase)+2, (y*tailleCase)+2, anchor=NW, image=image3)
                    listeImage[y][x] = case
                elif matriceT[y][x] == 4 : 
                    case = tableau.create_image((x*tailleCase)+2, (y*tailleCase)+2, anchor=NW, image=image4)
                    listeImage[y][x] = case
                elif matriceT[y][x] == 5 : 
                    case = tableau.create_image((x*tailleCase)+2, (y*tailleCase)+2, anchor=NW, image=image5)
                    listeImage[y][x] = case
                elif matriceT[y][x] == 6 : 
                    case = tableau.create_image((x*tailleCase)+2, (y*tailleCase)+2, anchor=NW, image=image6)
                    listeImage[y][x] = case
                elif matriceT[y][x] == 7 : 
                    case = tableau.create_image((x*tailleCase)+2, (y*tailleCase)+2, anchor=NW, image=image7)
                    listeImage[y][x] = case
                elif matriceT[y][x] == 8 : 
                    case = tableau.create_image((x*tailleCase)+2, (y*tailleCase)+2, anchor=NW, image=image8)
                    listeImage[y][x] = case
            elif T[y][x] == 2 : 
                case = tableau.create_image((x*tailleCase)+2, (y*tailleCase)+2, anchor=NW, image=imageCase)
                listeImage[y][x] = case
            elif (T[y][x] == 3) or (T[y][x]==4): 
                tableau.create_image((x*tailleCase)+2, (y*tailleCase)+2, anchor=NW, image=imageDrapeau)
                listeImage[y][x] = case

def affichageSingulier(posX, posY):
    global listeImage, tailleCase
    if T[posY][posX] == 0: 
        case = tableau.create_image((posX*tailleCase)+2, (posY*tailleCase)+2, anchor=NW, image=imageCase)
        listeImage[posY][posX] = case
    elif T[posY][posX] == 1 :
        if matriceT[posY][posX] == 0 : 
            case = tableau.create_image((posX*tailleCase)+2, (posY*tailleCase)+2, anchor=NW, image=imageCreusee)
            listeImage[posY][posX] = case
        elif matriceT[posY][posX] == 1 : 
            case = tableau.create_image((posX*tailleCase)+2, (posY*tailleCase)+2, anchor=NW, image=image1)
            listeImage[posY][posX] = case
        elif matriceT[posY][posX] == 2 : 
            case = tableau.create_image((posX*tailleCase)+2, (posY*tailleCase)+2, anchor=NW, image=image2)
            listeImage[posY][posX] = case
        elif matriceT[posY][posX] == 3 : 
            case = tableau.create_image((posX*tailleCase)+2, (posY*tailleCase)+2, anchor=NW, image=image3)
            listeImage[posY][posX] = case
        elif matriceT[posY][posX] == 4 : 
            case = tableau.create_image((posX*tailleCase)+2, (posY*tailleCase)+2, anchor=NW, image=image4)
            listeImage[posY][posX] = case
        elif matriceT[posY][posX] == 5 : 
            case = tableau.create_image((posX*tailleCase)+2, (posY*tailleCase)+2, anchor=NW, image=image5)
            listeImage[posY][posX] = case
        elif matriceT[posY][posX] == 6 : 
            case = tableau.create_image((posX*tailleCase)+2, (posY*tailleCase)+2, anchor=NW, image=image6)
            listeImage[posY][posX] = case
        elif matriceT[posY][posX] == 7 : 
            case = tableau.create_image((posX*tailleCase)+2, (posY*tailleCase)+2, anchor=NW, image=image7)
            listeImage[posY][posX] = case
        elif matriceT[posY][posX] == 8 : 
            case = tableau.create_image((posX*tailleCase)+2, (posY*tailleCase)+2, anchor=NW, image=image8)
            listeImage[posY][posX] = case
    elif T[posY][posX] == 2 : 
        case = tableau.create_image((posX*tailleCase)+2, (posY*tailleCase)+2, anchor=NW, image=imageCase)
        listeImage[posY][posX] = case
    elif (T[posY][posX] == 3) or (T[posY][posX]==4): 
        case = tableau.create_image((posX*tailleCase)+2, (posY*tailleCase)+2, anchor=NW, image=imageDrapeau)
        listeImage[posY][posX] = case

def creuserGraphique(event):
    global tailleCase, T, matriceT, nombresMines, posX, posY, Terminer, premierCreuser, longueur, hauteur, difficulte, posX, posY
    posX = ((event.x)-2)//tailleCase
    posY = ((event.y)-2)//tailleCase
    if Terminer == False:
        if premierCreuser == False:
            if T[posY][posX] == 0:
                creuser_recu(T, matriceT, posX, posY)
            elif T[posY][posX] == 2:
                Terminer = True
                lose()
        else: 
            if (T[posY][posX] == 0) and (matriceT[posY][posX] == 0):
                premierCreuser = False
                creuser_recu(T, matriceT, posX, posY)
            else:
                while ((T[posY][posX] != 0) and (T[posY][posX] != 1)) or (matriceT[posY][posX] != 0):
                    T, nombresMines = Int_jeu(longueur, hauteur, difficulte)
                    matriceT = mines_autour(T)
                creuser_recu(T, matriceT, posX, posY)
                premierCreuser = False
        winCondition()

def drapeauGraphique(event):
    posX = ((event.x)-2)//tailleCase
    posY = ((event.y)-2)//tailleCase
    if (T[posY][posX] == 0) or (T[posY][posX] == 2):
        poser_drapeau(T, posX, posY)
    elif (T[posY][posX] == 3) or (T[posY][posX] == 4):
        lever_drapeau(T, posX, posY)
    tableau.delete(listeImage[posY][posX])
    affichageSingulier(posX, posY)

def winCondition():
    global longueur, hauteur, N, nombresMines, minute, seconde, textScore, Terminer, texteVictoire, tableau
    if (longueur*hauteur) - N == nombresMines:
        Terminer = True
        if minute == 0: 
            texteVictoire = "Vous avez mis "+ str(seconde)+" secondes pour démineur le térrain, pour un total de "+str(textScore)+" points."
        elif minute == 1: 
            texteVictoire = "Vous avez mis une minute et "+ str(seconde)+" secondes pour démineur le térrain, pour un total de "+str(textScore)+" points."
        else:
            if seconde > 0:
                texteVictoire = "Vous avez mis "+str(minute)+" minutes et "+ str(seconde)+" secondes pour démineur le térrain, pour un total de "+str(textScore)+" points."
            else :
                texteVictoire = "Vous avez mis "+str(minute)+" minutes pour démineur le térrain, pour un total de "+str(textScore)+" points."
        for y in range(hauteur):            #suppresion des images de case sur les mines et les drapeaux sur les mines
            for x in range(longueur):
                if (T[y][x] == 2) or (T[y][x] == 4):
                    tableau.delete(listeImage[y][x])
        for y in range(hauteur):            #pour les remplacer par des images de mines
            for x in range (longueur):
                if T[y][x] == 2 : 
                    case = tableau.create_image((x*tailleCase)+2, (y*tailleCase)+2, anchor=NW, image=imageBombe)
                    listeImage[y][x] = case
                elif T[y][x] == 4: 
                    case = tableau.create_image((x*tailleCase)+2, (y*tailleCase)+2, anchor=NW, image=imageBombe)
                    listeImage[y][x] = case
        popUpVictoire()

def lose():
    global N, seconde, minute, textScore, Terminer, textePerte, posX, posY, tableau 
    Terminer = True
    if minute == 0: 
        textePerte = "Vous avez mis "+ str(seconde)+" secondes pour creuser "+str(N)+" cases, pour un total de "+str(textScore)+" points."
    elif minute == 1: 
        textePerte = "Vous avez mis une minute et "+ str(seconde)+" secondes pour creuser "+str(N)+" cases, pour un total de "+str(textScore)+" points."
    else:
        if seconde > 0:
            textePerte = "Vous avez mis "+str(minute)+" minutes et "+ str(seconde)+" secondes pour creuser "+str(N)+" cases, pour un total de "+str(textScore)+" points."
        else :
            textePerte = "Vous avez mis "+str(minute)+" minutes pour creuser "+str(N)+" cases, pour un total de "+str(textScore)+" points."
    for y in range(hauteur):                    #suppression des images de case sur les mines, les drapeaux mal placés et la mine creusée
        for x in range(longueur):
            if (T[y][x] == 2) or (T[y][x] == 3):
                tableau.delete(listeImage[y][x])
    for y in range (hauteur):                   
        for x in range (longueur):              #pour les remplacer par des images de mines, de drapeaux mal placés et de la mine creusée
            if T[y][x] == 2: 
                case = tableau.create_image((x*tailleCase)+2, (y*tailleCase)+2, anchor=NW, image=imageBombe)
                listeImage[y][x] = case
            elif T[y][x] == 3: 
                tableau.create_image((x*tailleCase)+2, (y*tailleCase)+2, anchor=NW, image=imageDrapeauMS)
                listeImage[y][x] = case
    tableau.delete(listeImage[posY][posX])      #suppression de l'image de la mine creusée
    case = tableau.create_image((posX*tailleCase)+2, (posY*tailleCase)+2, anchor=NW, image=imageMineCreusee) #pour la remplacer par une image de mine barrée
    listeImage[y][x] = case
    popUpPerte()


def menuPrincipal():
    buttonCommencer.grid(row=0, column=0)
    buttonQuitter.grid(row=1, column=0)
    
    labelIconeMenu.grid(row=0, column=0)
    boiteMenu.grid(row=0,column=1)          #pour centrer les boutons
    fenetreMenu.grid(row=0, column=0)

def menuOption():
    fenetreMenu.grid_forget()

    labelIconeOption = Label(boiteButton,image=imageIcone)
    labelIconeOption.grid(row=0, column=0)

    sliderLongueur.set(10)
    sliderHauteur.set(10)

    sliderLongueur.grid(row=0, column=0)
    sliderHauteur.grid(row=0, column=0)

    buttonDiff1.grid(row=0, column=0)
    buttonDiff2.grid(row=1, column=0)
    buttonDiff3.grid(row=2, column=0)

    buttonCommencerOption.grid(row=1, column=0)
    buttonQuitterOption.grid(row=2, column=0)

    boiteDiffOption.grid(row=0, column=1)

    boiteTroisiemeLigne.grid(row=1, column=0)
    boiteButton.grid(row=0, column=1)
    boiteConfig.grid(row=0, column=0)
    fenetreOption.grid(row=0, column=0)

def jeu():
    global debutTimer, longueur, hauteur, difficulte, T, matriceT, tableau, tailleCase, Terminer, premierCreuser, nombresMines, N

    tailleCase = 32
        
    longueur = 0
    hauteur = 0

    N = 0
    ValeurGet()
    
    longueurmax = tailleCase*longueur
    hauteurmax = tailleCase*hauteur

    fenetreOption.grid_forget()

    creationImage()

    labelIconeJeu = Label(fenetreOptionJeu, image=imageIcone)

    Terminer = False
    premierCreuser = True

    T, nombresMines = Int_jeu(longueur, hauteur, difficulte)
    matriceT = mines_autour(T)

    debutTimer = time.time()
    timer()
    score()

    tableau = Canvas(fenetreJeu, bg="#c0c0c0", width=longueurmax, height=hauteurmax)

    affichageGraphique()
    
    tableau.grid(row=0, column=0)

    labelIconeJeu.grid(row=0, column=0, sticky=W)
    labelTimer.grid(row=0, column=1)
    labelScore.grid(row=0, column=2)
    buttonQuitterJeu.grid(row=0, column=3, sticky=E)

    tableau.bind("<Button-1>", creuserGraphique)
    tableau.bind("<Button-3>", drapeauGraphique)

    fenetreJeu.grid(row=0, column=0)
    fenetreOptionJeu.grid(row=1, column=0)


def popUpVictoire():
    global fenetreFindeJeu, texteVictoire
    fenetreFindeJeu = Toplevel(fenetre)
    fenetreFindeJeu.title("Vous avez gagné!")
    fenetreFindeJeu.config(bg="#3ac424")

    labelVictoire = Label(fenetreFindeJeu, text=texteVictoire, bg="#3ac424")
    labelVictoire.grid(row=0, column=0)

    buttonRecommencerVictoire = Button(fenetreFindeJeu, text="Recommencer", command=lambda:recommencer())
    buttonQuitterPopUpV = Button(fenetreFindeJeu, text="Quitter", command=lambda:fenetre.destroy())

    buttonRecommencerVictoire.grid(row=1, column=0) 
    buttonQuitterPopUpV.grid(row=2, column=0)

def popUpPerte():
    global fenetreFindeJeu, textePerte
    fenetreFindeJeu = Toplevel(fenetre)
    fenetreFindeJeu.title("Vous avez perdu...")
    fenetreFindeJeu.config(bg="#e52727")

    labelPerte = Label(fenetreFindeJeu, text=textePerte, bg="#e52727")
    labelPerte.grid(row=0, column=0)

    buttonRecommencerPerte = Button(fenetreFindeJeu, text="Recommencer", command=lambda:recommencer())
    buttonQuitterPopUpP = Button(fenetreFindeJeu, text="Quitter", command=lambda:fenetre.destroy())

    buttonRecommencerPerte.grid(row=1, column=0) 
    buttonQuitterPopUpP.grid(row=2, column=0)

def recommencer():
    for y in range(hauteur):
            for x in range(longueur):
                tableau.delete(listeImage[y][x])
    fenetreJeu.grid_forget()
    fenetreOptionJeu.grid_forget()
    menuOption()
    fenetreFindeJeu.destroy()

def launchGame():
    global fenetre, fenetreMenu, imageIcone, labelIconeMenu, boiteMenu, boiteButton
    global buttonCommencer, buttonQuitter, sliderLongueur, sliderHauteur
    global difficulte, buttonDiff1, buttonDiff2, buttonDiff3
    global buttonCommencerOption, buttonQuitterOption, fenetreOptionJeu
    global fenetreJeu, buttonQuitterJeu, labelTimer, labelScore, labelFindeJeu
    global boiteDiffOption, boiteTroisiemeLigne, boiteConfig, fenetreOption

    fenetre = Tk()
    fenetre.title("Démineur")
    fenetre.iconbitmap("images/demineur.ico")
    fenetre.resizable(0,0)

    # fenètre pour le menu principal
    fenetreMenu = Frame(fenetre)                        
    # création de l'image
    imageIcone = PhotoImage(file="images/icone.png")      
    labelIconeMenu = Label(fenetreMenu, image=imageIcone)
    boiteMenu = Frame(fenetreMenu)
    buttonCommencer = Button(boiteMenu, text="Commencer le dénimeur", bg="#c0c0c0", command=menuOption)
    buttonQuitter = Button(boiteMenu, text="Quitter", bg="#c0c0c0", command=fenetre.destroy)


    # fenètre pour le menu pour configurer le démineur
    fenetreOption = Frame(fenetre)                      
    boiteConfig = LabelFrame(fenetreOption, text="Configuration du terrain")
    boiteTroisiemeLigne = Frame(boiteConfig)
    boiteDiffOption = LabelFrame(boiteTroisiemeLigne, padx=10, text="Difficulté")
    boiteButton = Frame(fenetreOption)

    sliderLongueur = Scale(boiteConfig, from_=5, to=50, length=250, tickinterval=5, troughcolor="#c0c0c0", orient=HORIZONTAL)
    sliderHauteur = Scale(boiteTroisiemeLigne, from_=5, to=30, tickinterval=5, troughcolor="#c0c0c0", length=100)

    # difficulte par défaut
    difficulte = 2          

    buttonDiff1 = Button(boiteDiffOption, text="Facile", bg="#c0c0c0", command=partial(SetDiff, 1))
    buttonDiff2 = Button(boiteDiffOption, text="Moyen", bg="#c0c0c0", command=partial(SetDiff, 2))
    buttonDiff3 = Button(boiteDiffOption, text="Difficile", bg="#c0c0c0", command=partial(SetDiff, 3))

    buttonCommencerOption = Button(boiteButton, text="Confirmer", bg="#c0c0c0", command=jeu)
    buttonQuitterOption = Button(boiteButton, text="Quitter", bg="#c0c0c0", command=fenetre.destroy)


    fenetreOptionJeu = Frame(fenetre)
    fenetreJeu = Frame(fenetre)
    buttonQuitterJeu = Button(fenetreOptionJeu, text="Quitter", command=fenetre.destroy)
    labelTimer = Label(fenetreOptionJeu)
    labelScore = Label(fenetreOptionJeu)


    fenetreFindeJeu = Frame(fenetre)
    labelFindeJeu = Label(fenetreFindeJeu)


    menuPrincipal()

    fenetre.mainloop()

if __name__ == "__main__":
    launchGame()