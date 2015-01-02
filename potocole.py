# -*- coding: utf-8 -*-
# code by :
# Andrès Franco

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
