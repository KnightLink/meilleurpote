class Board:
	# nodes sont de la forme [{speed=X,nbUnits=Y}]
	def __init__(self,nb_player = 0,nodes=[]):
	
		self.nodes = [] ;
		if nodes != [] :
			i = 0 ;
			for dict in nodes :
				i+=1 ;
				if 'speed' in dict :
					self.nodes.append(Node(i-1,-1,dict['speed']))
				else:
					self.nodes.append(Node(i-1))
				
				if 'owner' in dict :
					self.nodes[i-1].owner = dict['owner'] ;

				if 'nbUnits' in dict :
					self.nodes[i-1].units = dict['nbUnits'] ;

		self.nb_player = nb_player ;
		self.speed = 1 ;
		self.time = 0 ; #millisecondes
		
	def getEdge(self,node1,node2):
		#PRINT FOR DEBUG PURPOSES
		#print("GET_EDGE : ",node1.id, " + ", node2.id);
		for e in node1.edges :
			#print(e.node1.id,"  ",e.node2.id,"  ",node2.id);
			if (e.node1 == node2 or e.node2 == node2) :
				#print("RESULT : OK");
				return e ;
		#print("RESULT : SRYNO");
		return None ;
		
	def addEdges(self,edges): #list of tuples (node_id1,node_id2,dist)
		i=0 ;
		for tuple in edges :
			i+=1;
			Edge(i,self.nodes[tuple[0]],self.nodes[tuple[1]],tuple[2])
			
	def __str__(self):
		string = "" ;
		for node in self.nodes :
			string += "NODE"+str(node.id)+" "+str(node.units)+" UNITS ("+str(node.defunits)+" DEF) WITH "+str(node.productionSpeed)+" SPEED AND OWNER "+str(node.owner)+"\n";
		string += "CONNECTIONS :\n";
		edges = [] 
		for node in self.nodes :
			for e in node.edges :
				if e.id in edges :
					pass
				else :
					for bus in e.bus :
						if bus.destination == e.node1.id :
							string+= str(e.node2.id) + " GOING TO " + str(e.node1.id) + " WITH "+str(bus.units) +" UNITS (OWNER : "+ str(bus.owner) +", TIMESTAMP :"+ str(bus.time_start) +") \n" ;
						else :
							string+= str(e.node1.id) + " GOING TO " + str(e.node2.id) + " WITH "+str(bus.units) +" UNITS (OWNER : "+ str(bus.owner) +", TIMESTAMP :"+ str(bus.time_start) +") \n" ;
					edges.append(e.id);
		return string ;
		
	def updateCells(self,cells): #cells : list of tuples
		for c in cells :
			id = c[0]
			self.nodes[id].owner = c[1] ;
			self.nodes[id].units = c[2] ;
			self.nodes[id].defunits = c[3] ;
	
	def updateMoves(self,moves): #moves : liste de (src,dest,amount,owner,timestamp)
		for n in self.nodes :
			for e in n.edges :
				del e.bus[:]
				
		for move in moves :
			(source,dest,amount,owner,timestamp) = move
			self.getEdge(self.nodes[source],self.nodes[dest]).bus.append(Bus(owner,dest,amount,timestamp)) ;

		#print("EXISTING BUS : ",moves);
		
		
class Bus: # Vaisseau de transport d'unités
	def __init__(self,owner,destination,units,time_start):
		self.owner=owner
		self.destination=destination
		# destination === cell_id 
		
		self.units=units
		self.time_start=time_start
		
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
		self.units=0 ;
		self.defunits = 0 ;
		self.productionSpeed=production_speed
		
	def getAdjoining(self):
		adj=[]
		for edge in self.edges:
			if edge.node1==self:
				adj.append(edge.node2)
			else:
				adj.append(edge.node1)
		return adj
				
		
