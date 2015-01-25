from board import Board
import math
import potocole
class AI:
	def __init__(self,board,playerId = 0):
		self.board = board ;
		self.playerId = playerId ;
		self.orders = [] ; # liste de STRING
		
	def evalBoard(self,playerNb):
		#GLOBALS
		VALUE_UNIT = 0.1
		VALUE_NODE = 0.3
		VALUE_NODE_SPEED = 0.3
		VALUE_SURRONDINGS = 1 # surroundings = x * ratio avec ratio = 0 si tout seul, 1 si uniquement des alliés autour (variable si ni 0 ni 1)
		
		RATIO_ISOLATED = 0 # se multiplie à la value des unités si le point est entouré uniquement d'alliés
		
		playersValue = {} ;
		for i in range(self.board.nb_player):
			playersValue[i] = [0,0,0] ; # playersValue[num] = (nbunit,nbnode)
		for n in self.board.nodes :
			if n.owner != -1 :
				nbOwned = 0
				for adjNode in n.getAdjoining():
					if adjNode.owner == n.owner:
						nbOwned += 1
				playersValue[n.owner][2] += VALUE_SURRONDINGS*nbOwned/len(n.getAdjoining())
				# si entouré d'alliés, on applique le ratio surrounded
				if playersValue[n.owner][2]==VALUE_SURRONDINGS:
					surrounded=RATIO_ISOLATED
				else:
					surrounded=1
				playersValue[n.owner][0] += n.units * VALUE_UNIT * surrounded;
				playersValue[n.owner][1] += VALUE_NODE * ((n.productionSpeed-1) * VALUE_NODE_SPEED + 1) 
				
				
						
		sum_value = 0 ;
		for key in playersValue:
			if key != playerNb :
				sum_value += playersValue[key][0] * VALUE_UNIT ; 
				sum_value += playersValue[key][1] * VALUE_NODE ;
				sum_value += playersValue[key][2] * VALUE_SURRONDINGS ;
				
		
		# return l'indice de progression
		sum_value /= (self.board.nb_player - 1) ;
		total_player_value = playersValue[playerNb][0]+playersValue[playerNb][1] ; 
		return total_player_value / sum_value ;
		
	def createOrders(self):
		# STRATEGIE
		# Ecart max = Poids le plus grand - Poids le plus faible
		# Relevance = (Poids du noeud - Poids le plus faible) / Ecart max
		# Paramètres
		RELEVANCE_MIN=0.2
		RELEVANCE_TOTAL=0.8
		COEF_NEED_EMPTY=0.5
		# Table des poids
		board_weight=self.evalBoardByNodeWeight(self.board.nb_player)
		# Determination du maximum de poids et de l'écart max
		maxw=0
		self.evalBoardByNodeWeight(self.board.nb_player,True)
		for n in board_weight.values():
				if n>maxw:
		                    maxw=n
		minw=maxw
		for n in board_weight.values():
		    if n<minw:
                        minw=n
		ecart=maxw-minw
		# Determination des noeuds possedes
		own_nodes=[]
		for n in self.board.nodes:
		    if n.owner==self.playerId:
                        own_nodes.append(n)
		# Listage des noeuds à explorer (possedes + adjacents)
		nodes_to_explore=[]
		for n in own_nodes:
                    nodes_to_explore.append(n)
                    print("NODE"+str(n.id)+" TO EXPLORE")
                    adj=n.getAdjoining()
                    for m in adj:
                        if m not in own_nodes:
                            print("NODE"+str(m.id)+" TO EXPLORE")
                            nodes_to_explore.append(m)
                # Listage des noeuds à vider
		nodes_to_empty=[]
		for n in own_nodes:
		    relevance=(board_weight[n.id]-minw)/ecart
		    if relevance<RELEVANCE_MIN:
                        nodes_to_empty.append(n)
                        print("NODE"+str(n.id)+" TO EMPTY")
		# Dispatch + Elimination des nodes peu importants (Relevance < x%)
		for n in nodes_to_explore:
                    print("EXPLORING DESTINATION NODE"+str(n.id))
                    relevance=(board_weight[n.id]-minw)/ecart
                    units_max=10+10*n.productionSpeed
                    if relevance < RELEVANCE_MIN:
                        nodes_to_explore.remove(n)
                        print("NODE"+str(n.id)+" NOT RELEVANT")
                    else:
                        target_adj=n.getAdjoining()
                        print(target_adj)
                        dangerless=[maxw,None]
                        for m in target_adj: # Choix du point de départ
                            print("EXPLORING SOURCE NODE"+str(m.id))
                            if board_weight[m.id]<=dangerless[0] and m in own_nodes:
                                coef=1
                                if m in nodes_to_empty:
                                    coef=COEF_NEED_EMPTY
                                print(str(dangerless[0]))
                                dangerless=[board_weight[m.id]*coef,m]
                                print(str(dangerless[0]))
                                print("NODE"+str(m.id)+" RANKED DANGERLESS")
                                
                            else:
                                print("NODE"+str(m.id)+" NOT INTERESTING SOURCE")
                        if dangerless[1]!=None:
                            print("CONSIDERING NODE"+str(dangerless[1].id)+" : CHECKING RELEVANCE")
                            if relevance >= RELEVANCE_TOTAL:
                                amount=100
                            else:
                                amount=math.floor(relevance*100)
                            
                            if math.floor((amount/100)*dangerless[1].units)+n.units>units_max:
                                amount=math.floor((units_max-n.units)*100/dangerless[1].units)
                            self.orders.append(potocole.encodeOrder(dangerless[1].id,n.id,amount))
                            print("NODE"+str(dangerless[1].id)+" SENT TO NODE"+str(n.id)+" ("+str(amount)+"%)")
                        else:
                            print("NODE"+str(n.id)+" ORDER CANCELLED")
					
			
		

		#self.orders.append(potocole.encodeOrder(0,1,90)); FROM, TO, AMOUNT EN %
	
	def evalBoardByNodeWeight(self,playerNb,printing=False):
		board_weight=dict()
		for n in self.board.nodes:
			if printing==False:
				board_weight[n.id]=self.evalNodeWeight(n,playerNb)
			else:
				print(str(n.id)+" : "+str(self.evalNodeWeight(n,playerNb)))
		return board_weight

	def evalNodeWeight(self,node,owner):
		sum =0
		max_units=node.productionSpeed*10+10
		WEIGHT_SELF_ALLY= 1; # superieur a WEIGHT SELF ENEMY: tendence à la defense, sinon YOLO
		WEIGHT_SELF_ENEMY= 30; # superieur a WEIGHT SELF ALLY : tendence à l'attaque
		WEIGHT_ALLIES= -30;
		WEIGHT_NEUTRAL= 15;
		WEIGHT_ENEMIES= 30;
		WEIGHT_RATIO_PRODUCTION= 5;
		WEIGHT_PER_UNIT = 0.2 ;
		CEILING_MAX_UNITS = 0.3 # >x% du nombre max du points si possédé : moins important
		WEIGHT_LOSS_MAX_UNITS = -50
		WEIGHT_SURROUNDED_BY_ALLIES = -150
		WEIGHT_ONE_TARGET = -100
		
		if (owner == node.owner):
			sum+=WEIGHT_SELF_ALLY ;
			if node.units > CEILING_MAX_UNITS*max_units:
                            sum+=WEIGHT_LOSS_MAX_UNITS*(node.units/max_units)
		else :
			sum+=WEIGHT_SELF_ENEMY+max_units-node.units ;
		
		#TODO : 5 et 6 bugue pour joueur 3 !!!!!
		adjoining = node.getAdjoining()
		number_allies_adj=0
		for obj in adjoining :
                    if obj.owner == owner :
                        number_allies_adj+=1
                        if node.owner == owner or node.owner == -1 :
                            sum += WEIGHT_ALLIES + WEIGHT_RATIO_PRODUCTION* (1-obj.productionSpeed) ;
                        else:
                            sum -= WEIGHT_ALLIES *(1+WEIGHT_PER_UNIT*node.units)
                    elif obj.owner == -1 :
                        sum += WEIGHT_NEUTRAL + WEIGHT_RATIO_PRODUCTION* (1-obj.productionSpeed);
                    else :
                        if node.owner == owner or node.owner == -1 :
                            sum += WEIGHT_ENEMIES *(1+WEIGHT_PER_UNIT*node.units) + WEIGHT_RATIO_PRODUCTION* (1-obj.productionSpeed)  ;
                        else :
                            sum -= WEIGHT_ENEMIES *(1+WEIGHT_PER_UNIT*obj.units) ;
                            
		if number_allies_adj==len(adjoining):
		    sum+=WEIGHT_SURROUNDED_BY_ALLIES
		if number_allies_adj==len(adjoining)-1:
		    sum+=WEIGHT_ONE_TARGET
		return sum ;
		
		
