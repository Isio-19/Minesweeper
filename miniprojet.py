import time

from random import randint 

def afficher(T):
    for y in range(len(T)):
        for x in range(len(T[0])):
            print(T[y][x], end=" ")
        print("\n", end="")

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
                if T[y-1][x-1] == 2: mines_proximite += 1
            if y != 0:
                if T[y-1][x] == 2: mines_proximite += 1
            if y != 0 and x != len(T[0])-1:
                if T[y-1][x+1] == 2: mines_proximite += 1
            if x != 0:
                if T[y][x-1] == 2: mines_proximite += 1
            if x != len(T[0])-1:
                if T[y][x+1] == 2: mines_proximite += 1
            if y != len(T)-1 and x != 0:
                if T[y+1][x-1] == 2: mines_proximite += 1
            if y != len(T)-1 :
                if T[y+1][x] == 2: mines_proximite += 1
            if y != len(T)-1 and x != len(T[0])-1:
                if T[y+1][x+1] == 2: mines_proximite += 1
            matriceT[y][x] = mines_proximite
    return matriceT

def affichage(T,matriceT):
    print(end="    ")
    for x in range(len(T[0])): 
        if x < 10: print(x, end="  ")
        else: print(x, end=" ")
    print("\n")
    for y in range(len(T)):
        if y < 10: print(y, end="   ")
        else : print(y, end="  ")
        for x in range(len(T[0])):
            if T[y][x] == 0: print("?", end="  ") 
            elif T[y][x] == 1:
                if matriceT[y][x] == 0: print(".", end="  ")
                else: print(matriceT[y][x], end="  ")
            elif T[y][x] == 3 or T[y][x] == 4: print("d", end="  ")
            elif T[y][x] == 2: print("?", end="  ")
        print("\n", end="")
    
def poser_drapeau(T,x,y):
    if T[y][x] == 0:
        T[y][x] = 3
    elif T[y][x] == 2:
        T[y][x] = 4

def lever_drapeau(T,x,y):
    if T[y][x] == 3:
        T[y][x] = 0
    elif T[y][x] == 4:
        T[y][x] = 2

def creuser(T,matriceT,x,y):
    global N                #j'ai mis cela parce que sinon, la variable N revient toujours à 0 bizarement
    if T[y][x] == 0:
        T[y][x] = 1
        N += 1
        return True
    elif T[y][x] == 2: return False

def creuser_recu(T,matriceT,x,y):
    global N
    if matriceT[y][x] == 0 and T[y][x] == 0:
        T[y][x] = 1
        N += 1 
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
        return creuser(T,matriceT,x,y,)

def score(N,TempsPris):
    points = (N*1000)-((TempsPris)*200)
    return points

def launchGame():
    global N
    continuer = True
    while continuer == True:
        x = int(input("Donner la longueur du terrain : "))
        y = int(input("Donner la hauteur du terrain : "))
        difficulte = int(input("Choisisser une difficulté entre 1 et 3 : "))
        print("")
        T, mines = Int_jeu(x,y,difficulte)
        matriceT = mines_autour(T)
        N = 0
        affichage(T,matriceT)
        debutTime = time.time()
        x_case = int(input("Où voulez-vous initier la partie ? (X) "))
        y_case = int(input("Où voulez-vous initier la partie ? (Y) "))
        while matriceT[y_case][x_case] != 0:        #Ce while sert à toujours commencer la partie sur une partie de terrain découvert
            T, mines = Int_jeu(x,y,difficulte)
            matriceT = mines_autour(T)
        creuser_recu(T,matriceT,x_case,y_case)
        terminer = False
        while terminer == False:
            print("")
            affichage(T,matriceT)
            demandeAction = str(input("Voulez-vous creuser, poser / lever un drapeau ? (C,D) "))
            x_case = int(input("Où voulez-vous faire cette action (X) ? "))
            y_case = int(input("Où voulez-vous faire cette action (Y) ? "))
            if (demandeAction == "C") or (demandeAction == "c"):
                if T[y_case][x_case] == 1: 
                    print("")
                    print("Cette case a déjà été creusée")
                elif T[y_case][x_case] == 3 or T[y_case][x_case] == 4: 
                    print("")
                    print("Cette case a un drapeau")
                else:
                    case = creuser_recu(T,matriceT,x_case,y_case)
                    if case == False :
                        finTime = time.time()
                        TempsPris = int(finTime - debutTime)
                        print("")
                        print(f"Vous avez creusé une mine! Vous avez perdu avec un score de {score(N, TempsPris)}")
                        terminer = True
            elif demandeAction == "D" or demandeAction == "d":
                if T[y_case][x_case] == 3 or T[y_case][x_case] == 4:
                    lever_drapeau(T,x_case,y_case)
                elif T[y_case][x_case] == 0 or T[y_case][x_case] == 2:
                    poser_drapeau(T,x_case,y_case)
                else: 
                    print("")
                    print("Cette case à déjà été creusée")
            else: 
                print("Commande incorrecte, veuillez réessayer")
            if N == ((x*y)-mines):
                finTime = time.time()
                TempsPris = int(finTime - debutTime)
                print("")
                print(f"Vous avez réussi à deminer le terrain! Votre score est de {score(N, TempsPris)} points.")
                terminer = True
        demandeContinuer = str(input("Voulez-vous continuer ? (Y/N) "))
        if (demandeContinuer == "N") or (demandeContinuer == "n"):
            continuer = False
    

if __name__ == "__main__":
    launchGame()