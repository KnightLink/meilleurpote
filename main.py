import re
from board import Board 
from AI import AI
from node import Node
from edge import Edge


print("tapez 1 pour test le board, 2 pour test le regex")
which = input() ;
if (which == "1") :
    mainBoard=Board(3)
    n1=Node(1,1)
    n2=Node(2,1)
    n3=Node(3,1)
    
    n4=Node(4,2,3)
    n5=Node(5,2)
    n6=Node(6,2)
    
    n7=Node(7,3)
    n8=Node(8,3)
    n9=Node(9,2)
    
    n10=Node(10,1)
    
    n1.units=10
    n2.units=15
    n3.units=15
    
    n4.units=10
    n5.units=20
    n6.units=20
    
    n7.units=25
    n8.units=20
    n9.units=5
    
    n10.units=5
    
    mainBoard.nodes=(n1,n2,n3,n4,n5,n6,n7,n8,n9,n10)
    
    e1=Edge(1,n1,n2,2000)
    e2=Edge(2,n1,n3,2000)
    
    e3=Edge(3,n4,n5,2000)
    e4=Edge(4,n4,n6,2000)
    
    e5=Edge(5,n7,n8,2000)
    e6=Edge(6,n7,n9,2000)
    
    e7=Edge(7,n2,n10,3000)
    e8=Edge(8,n3,n10,3000)
    
    e9=Edge(9,n5,n10,3000)
    e10=Edge(10,n6,n10,3000)
    
    e11=Edge(11,n8,n10,3000)
    e12=Edge(12,n9,n10,3000)
    
    ai=AI(mainBoard);
    
    print(ai.evalBoard(1))
    print(ai.evalBoard(2))
    print(ai.evalBoard(3))
    
    print(ai.evalBoardByNodeWeight(2))
elif (which == "2") :
    string = "INIT20ac18ab-6d18-450e-94af-bee53fdc8fcaTO6[2];1;3CELLS:1(23,9)'2'30'8'I,2(41,55)'1'30'8'II,3(23,103)'1'20'5'I;2LINES:1@3433OF2,1@6502OF3"
    matchObj = re.search(r'^INIT([0-9abcdef\-]*)TO(\d+)\[(\d+)];(\d);([^;]*);([^;]*)$',string)
    match_id = "" ;
    nombre_joueurs = 0 ;
    numero_joueur = 0 ;
    cells_string = "" ;
    lines_string = "" ;
    speed = 1 ;
    
    if matchObj:
        print("match!")
        match_id = matchObj.group(1);
        nombre_joueurs = int(matchObj.group(2));
        numero_joueur = int(matchObj.group(3));
        speed = int(matchObj.group(4));
        cells_string = matchObj.group(5);
        lines_string = matchObj.group(6);
        print(match_id)
        print("nombre de joueurs :",nombre_joueurs)
        print("numero_joueur :",numero_joueur)
        print("vitesse :",speed)
        print("cells :", cells_string);
        print("lines :", lines_string);
        
        # utiliser re.findall pour cells et lines
        
    else:
        print("No match !")
        
        
        
"""
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
"""