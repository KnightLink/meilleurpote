import node, bus

class Edge: # Arete
    def __init__(self,id,node1,node2,length):
        self.id=id
        self.node1=node1
        self.node2=node2
        self.bus=[]
        self.node1.edges.append(self)
        self.node2.edges.append(self)
        self.length=length