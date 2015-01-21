# -*- coding: utf-8 -*-
# code by :
# Andrès Franco


import re
from AI import AI

from board import * 

def initStringToAI(string):
	
	matchObj = re.search(r'^INIT([0-9abcdef\-]*)TO(\d+)\[(\d+)];(\d);([^;]*);([^;]*)$',string)
	nbPlayers = int(matchObj.group(2));
	playerId = int(matchObj.group(3));
	speed = int(matchObj.group(4));
	cells_string = matchObj.group(5);
	lines_string = matchObj.group(6);
	liste_node = re.findall("(\d+\(\d+\,\d+\)\'\d+\'\d+\'\d+\'I+)",cells_string);
	l_n=[] #liste des Nodes
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
	l_e =[]; # liste des Edges
	for i in range (len(liste_edge)):
		information=re.search("([0-9]+)@([0-9]+)OF([0-9]+)",liste_edge[i])
		l_e.append((int(information.group(1)),int(information.group(3)),int(information.group(2))));
	
	print(l_e);
	
	board = Board(nbPlayers,l_n);
	
	board.addEdges(l_e);
	
	
	return AI(board,playerId) ;
