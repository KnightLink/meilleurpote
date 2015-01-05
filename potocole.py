# -*- coding: utf-8 -*-
# code by :
# Andrès Franco

'''
import re

string = "INIT20ac18ab-6d18-450e-94af-bee53fdc8fcaTO6[2];1;3CELLS:1(23,9)'2'30'8'I,2(41,55)'1'30'8'II,3(23,103)'1'20'5'I;2LINES:1@3433OF2,1@6502OF3"
matchObj = re.search(r'^INIT([0-9abcdef\-]*)TO(\d+)\[(\d+)];(\d);([^;]*);([^;]*)$',string)
match_id = "" ;
nombre_joueurs = 0 ;
numero_joueur = 0 ;
cells_string = "" ;
lines_string = "" ;
speed = 1 ;
#variable_aux=re.findall(r"CELLS:([0-9\(,\)\']*I+(,|;))",string)
liste=re.findall("(\d+\(\d+\,\d+\)\'\d+\'\d+\'\d+\'I+)",string)


l=[]
for i in range (len(liste)):
    l.append([])
    
for i in range (len(liste)):
    
    information=re.search("(\d)(\(\d+,\d+\))\'(\d+)\'(\d+)\'(\d+)\'([I]+)",liste[i])
    l[i].append(int(information.group(1)))
    l[i].append(eval(information.group(2)))
    l[i].append(int(information.group(3)))
    l[i].append(int(information.group(4)))
    l[i].append(int(information.group(5)))
    print(information.group(6))
    vitesse = 1;    
    if "I" == information.group(6) :
        vitesse=1
    if "II" == information.group(6) :
        vitesse=2
    if "III" == information.group(6):
        vitesse=int(3)
    
    l[i].append(vitesse)


print("match!")
match_id = matchObj.group(1);
nombre_joueurs = int(matchObj.group(2));
numero_joueur = int(matchObj.group(3));
speed = int(matchObj.group(4));
cells_string = matchObj.group(5);
lines_string = matchObj.group(6);
print(match_id)
print("nombre de joueurs :",nombre_joueurs)
print("numero_joueur : ",numero_joueur)
print("vitesse : ",speed)
print( "cells :",cells_string);  
print("lines :", lines_string);
'''
'''
 resultat attendu : 
 variable nombre_de_joueurs = 6
 variable numero_joueur = 2
 variable vitesse = 1
 double tableau cells constitue de la maniere suivante :
 cells[#NUMERO_CELL][#NUMERO_PROPRIETE] = valeur ;
 avec
 #NUMERO_PROPRIETE :
 0 : ID de la cellule
 1 : tuple contenant les coordonees (x,y)
 2 : radius
 3 : offsize
 4 : defensive_size
 5 : vitesse de production (entier), qui vaut soit 1, soit 2, soit 3
 
 lines :
 defini sous un tableau : lines[#NUMERO_LINE][#NUMERO_PROP]
 avec #NUMERO_PROP :
 1 : premiere cellule id
 2 : distance (entier)
 3 : seconde celulle id

par exemple resultat attendu pour les cellules :
[[1,(23,9),2,30,8,1],[2,(41,55),1,30,8,2],[3,(23,103),1,20,5,1]] 

'''


from board import * 

def initStringToBoard(string):

    matchId = "" ;
    
    nbPlayers = 2 ;
    #nombre de joueurs

    playerId = 0 ;
    #numero du joueur
    
    speed = 1 ;
    #vitesse de jeu    
    
    nodes = [] ;
    # contient une liste d'objets Node 
    
    edges = [] ;
    # contient une liste d'objets Edge
    
    board = Board(nbPlayers);
    
    
    return board ;
