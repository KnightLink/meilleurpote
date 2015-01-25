# -*- coding: utf-8 -*-
# code by :
# Andrès Franco


import re
from AI import *

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
	#print(l_n);
	liste_edge = re.findall("([0-9]+@[0-9]+OF[0-9]+)",lines_string);
	l_e =[]; # liste des Edges
	for i in range (len(liste_edge)):
		information=re.search("([0-9]+)@([0-9]+)OF([0-9]+)",liste_edge[i])
		l_e.append((int(information.group(1)),int(information.group(3)),int(information.group(2))));
	
	#print(l_e);
	return (nbPlayers,playerId,l_n,l_e) ;


def stateToTupleLists(state_string): #board est envoye par reference
	matchObj = re.search(r'^STATE[\w-]+;\d+CELLS:([^;]*);\d+MOVES:?([^:]*)$',state_string)
	string_cells = matchObj.group(1);
	string_moves = matchObj.group(2);
	
	list_cells= [];
	list_moves= [];
	
	liste_node = re.findall("(\d+\[-?\d+\]\d+\'\d+)",string_cells);
	for i in range (len(liste_node)):
		
		information = re.search("(\d+)\[(-?\d+)\](\d+)\'(\d+)",liste_node[i]);
		id = int(information.group(1)) ;
		owner = int(information.group(2))
		offsize = int(information.group(3))
		defsize = int(information.group(4))
		
		list_cells.append((id,owner,offsize,defsize));

	liste_line = re.findall("(?:,|^)([^,]+)",string_moves);

	for i in range (len(liste_line)):
		
		information = re.search("(\d+)((?:<|>)[^,]*)(\d+)(?:,|$)",liste_line[i]);
		node1 = int(information.group(1)) ;
		bus = information.group(2) ;
		node2 = int(information.group(3))
		all_bus = re.findall("([^']*)'",bus)
		
		for j in range(len(all_bus)):
			bus_data = re.search("(>|<)(\d+)\[(\d+)\]@(\d+)",all_bus[j]);
			bus_direction = bus_data.group(1);
			bus_units = int(bus_data.group(2));
			bus_owner = int(bus_data.group(3));
			bus_timestamp = int(bus_data.group(4));
			if ( bus_direction == ">" ):
				list_moves.append((node1,node2,bus_units,bus_owner,bus_timestamp));
			else :
				list_moves.append((node2,node1,bus_units,bus_owner,bus_timestamp));
		
		
	#print("LISTCELLSMOVES : ",list_cells,list_moves);
	return (list_cells,list_moves);
	#print("Cells  :",string_cells);
	#print("Moves  :",string_moves);
	
def encodeOrder(src_cell,dest_cell,amount=100): #amount en %
	return "MOV"+str(amount)+"FROM"+str(src_cell)+"TO"+str(dest_cell) ;
