import node.py
import bus.py

class Edge: # Arete
    def __init__(self,id,node1,node2):
        self.id=id
        self.node1=node1
        self.node2=node2
        self.bus=[]