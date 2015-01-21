import re
from board import *
from AI import AI
import potocole



print("tapez 1 pour test le board, 2 pour test le regex")
which = input() ;
if (which == "1") :

	
	mainBoard=Board(3,[
	{'nbUnits':10,'owner':0},
	{'nbUnits':15,'owner':0},
	{'nbUnits':15,'owner':0},
	{'nbUnits':10,'owner':1,'speed':3},
	{'nbUnits':20,'owner':1},
	{'nbUnits':20,'owner':1},
	{'nbUnits':25,'owner':2},
	{'nbUnits':20,'owner':2},
	{'nbUnits':5,'owner':1},
	{'nbUnits':5,'owner':0}
	])
	mainBoard.addEdges([
	(1,2,2000),
	(1,3,2000),
	(4,5,2000),
	(4,6,2000),
	(7,8,2000),
	(7,9,2000),
	(2,10,3000),
	(3,10,3000),
	(5,10,3000),
	(6,10,3000),
	(8,10,3000),
	(9,10,3000)]);
	
	ai=AI(mainBoard);
	print(mainBoard);
	
	print(ai.evalBoard(0))
	print(ai.evalBoard(1))
	print(ai.evalBoard(2))
	
	print(ai.evalBoardByNodeWeight(1))
	

elif (which == "2") :
	string = "INIT20ac18ab-6d18-450e-94af-bee53fdc8fcaTO6[2];1;3CELLS:1(23,9)'2'30'8'I,2(41,55)'1'30'8'II,3(23,103)'1'20'5'I;2LINES:1@3433OF2,1@6502OF3"
	matchObj = re.search(r'^INIT([0-9abcdef\-]*)TO(\d+)\[(\d+)];(\d);([^;]*);([^;]*)$',string)
	nbPlayers = int(matchObj.group(2));
	playerId = int(matchObj.group(3));
	speed = int(matchObj.group(4));
	cells_string = matchObj.group(5);
	lines_string = matchObj.group(6);
	liste_node = re.findall("(\d+\(\d+\,\d+\)\'\d+\'\d+\'\d+\'I+)",cells_string);
	l_n=[]
	for i in range (len(liste_node)):
		l_n.append({})
		information=re.search("(\d)(\(\d+,\d+\))\'(\d+)\'(\d+)\'(\d+)\'([I]+)",liste_node[i])
		


		vitesse = 1;
		if "I" == information.group(6) :
			vitesse=1
		if "II" == information.group(6) :
			vitesse=2
		if "III" == information.group(6):
			vitesse=3
		
		l_n[i]['speed'] = vitesse ;
	print(l_n);
	liste_edge = re.findall("([0-9]+@[0-9]+OF[0-9]+)",lines_string);
	l_e =[];
	for i in range (len(liste_edge)):
		information=re.search("([0-9]+)@([0-9]+)OF([0-9]+)",liste_edge[i])
		l_e.append((int(information.group(1)),int(information.group(3)),int(information.group(2))));
	
	print(l_e);
		
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
