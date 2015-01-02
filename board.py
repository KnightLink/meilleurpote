class Board:
    def __init__(self,nb_player = 0):
        self.nodes = [] ;
        self.nb_player = nb_player ;
        self.speed = 1 ;
        self.time = 0 ; #millisecondes
        
class Bus: # Vaisseau de transport d'unités
    def __init__(self,owner,direction,units,progress):
        self.owner=owner
        self.direction=direction
        self.units=units
        self.progress=progress
		
class Edge: # Arete
    def __init__(self,id,node1,node2,length):
        self.id=id
        self.node1=node1
        self.node2=node2
        self.bus=[]
        self.node1.edges.append(self)
        self.node2.edges.append(self)
        self.length=length
		
class Node: # Noeud
    def __init__(self,id,owner=0,production_speed=1):
        self.id=id
        self.edges=[]
        self.owner=owner # -1 = neutre
        self.units=0
        self.productionSpeed=production_speed
        
    def getAdjoining(self):
        adj=[]
        for edge in self.edges:
            if edge.node1==self:
                adj.append(edge.node2)
            else:
                adj.append(edge.node1)
        return adj
                
        
