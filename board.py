class Board:
	# nodes sont de la forme [{speed=X,nbUnits=Y}]
	def __init__(self,nb_player = 0,nodes=[]):
	
		self.nodes = [] ;
		if nodes != [] :
			i = 0 ;
			for dict in nodes :
				i+=1 ;
				if 'speed' in dict :
					self.nodes.append(Node(i,-1,dict['speed']))
				else:
					self.nodes.append(Node(i))
				
				if 'owner' in dict :
					self.nodes[i-1].owner = dict['owner'] ;

				if 'nbUnits' in dict :
					self.nodes[i-1].units = dict['nbUnits'] ;

		self.nb_player = nb_player ;
		self.speed = 1 ;
		self.time = 0 ; #millisecondes
		
	def addEdges(self,edges): #list of tuples (node_id1,node_id2,dist)
		i=0 ;
		for tuple in edges :
			i+=1;
			Edge(i,self.nodes[tuple[0]-1],self.nodes[tuple[1]-1],tuple[2])
			
	def __str__(self):
		string = "" ;
		for node in self.nodes :
			string += "NODE"+str(node.id)+" "+str(node.units)+" UNITS WITH "+str(node.productionSpeed)+" SPEED AND OWNER "+str(node.owner)+"\n";
		return string ;
			
			
		
		
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
	def __init__(self,id,owner=-1,production_speed=1):
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
				
		
