from node import Node
from edge import Edge

class Board:
    def __init__(self,nb_player = 0):
        self.nodes = [] ;
        self.nb_player = nb_player ;
        self.speed = 1 ;
        self.time = 0 ; #millisecondes
        