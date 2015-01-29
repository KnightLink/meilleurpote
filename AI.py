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
        
    def createOrders(self,idstrat=1):
        if idstrat==1:
            self.strat_relevance()
        if idstrat==2:
            self.strat_direction()
            
    def strat_direction(self):
        # STRATEGIE DIRECTIONS (couplage ordres directs + poids)
        # Paramètres
        CEILING_TO_EMPTY=0.8 # ça * maxunits = palier pour lequel noeud considéré à vider
        DISPATCH_ORDER=["conquer","protect","provide","attack"] # ordre de traitement (NE PAS INCLURE OSEF OU EMPTY)
        AMOUNT_PROTECT=80
        AMOUNT_PROVIDE=50
        AMOUNT_ATTACK=90
        AMOUNT_CONQUER=80
        # Table des poids
        board_weight=self.evalBoardByNodeWeight(self.playerId)
        # Initialisation dictionnaire des ordres
        board_orders=dict()
        board_rappel=dict()
        for n in self.board.nodes:
            board_orders[n.id]="osef"
            board_rappel[n.id]=n
        # Répartition des points
        for n in self.board.nodes:
            adj=n.getAdjoining()
            nbenemyadj=0
            nbpoteadj=0
            # Points alliés
            if n.owner==self.playerId:
                for a in adj:
                    if a.owner != self.playerId and a.owner!=-1:
                        nbenemyadj+=1
                        print("NODE"+str(n.id)+" nbenemy+1 grace a NODE"+str(a.id))
                    if a.owner == self.playerId:
                        nbpoteadj+=1
                if nbenemyadj<=1:
                    if nbenemyadj==1 or nbenemyadj<=math.floor(nbpoteadj/2+0.51):
                        board_orders[n.id]="provide"
                    if n.units>=(n.productionSpeed*10+10)*CEILING_TO_EMPTY or nbenemyadj==0:
                        board_orders[n.id]="empty"
                if len(adj)>=3 and nbenemyadj==(len(adj)-1):
                    board_orders[n.id]="protect"
                    
            # Points ennemis
            if n.owner!=self.playerId and n.owner!=-1:
                for a in adj:
                    if a.owner == self.playerId:
                        nbenemyadj+=1 # nbenemy, mais on parle du joueur qu'on controle
                        print("NODE"+str(n.id)+" nbenemy+1 grace a NODE"+str(a.id))
                if nbenemyadj>=1:
                    board_orders[n.id]="attack"
                    
            # Points neutres
            if n.owner==-1:
                nbotheradj=0
                for a in adj:
                    if a.owner == self.playerId:
                        nbenemyadj+=1 # nbenemy, mais on parle du joueur qu'on controle
                        print("NODE"+str(n.id)+" nbenemy+1 grace a NODE"+str(a.id))
                    if a.owner != self.playerId and a.owner != -1:
                        nbotheradj+=1 # autres joueurs
                        print("NODE"+str(n.id)+" nbother+1 grace a NODE"+str(a.id))
                if nbenemyadj==len(adj) or nbenemyadj>nbotheradj:
                    board_orders[n.id]="conquer"
                    
        
        # Verif
        print(board_orders)
        # DISPATCH
        for order in DISPATCH_ORDER:
            # Creation de la liste d'attente et la liste des noeuds "empty"
            queue=[]
            empty=[]
            osef_ally=[]
            provide=[]
            for ids in board_orders.keys():
                if board_orders[ids]==order:
                    queue.append(ids)
                if board_orders[ids]=="empty":
                    empty.append(ids)
                if board_orders[ids]=="osef" and board_rappel[ids].owner==self.playerId:
                    osef_ally.append(ids)
                if board_orders[ids]=="provide":
                    provide.append(ids)
            # Exploration
            for nid_empty in empty:
                node=board_rappel[nid_empty]
                adj=node.getAdjoining()
                if len(adj)==1:
                    self.orders.append(potocole.encodeOrder(nid_empty,adj[0].id,100))
                
            for nid in queue: # nid = n ID
                node=board_rappel[nid]
                adj=node.getAdjoining()
                queue_empty=[]
                queue_osef=[]
                queue_provide=[]
                for a in adj:
                    if a.id in empty:
                        queue_empty.append(a.id)
                    if a.id in osef_ally:
                        queue_osef.append(a.id)
                    if a.id in provide:
                        queue_provide.append(a.id)
                        
                if order=="protect":
                    if len(queue_empty)==1:
                        self.orders.append(potocole.encodeOrder(queue_empty[0],nid,AMOUNT_PROTECT))
                    elif len(queue_empty)>1:
                        best=[queue_empty[0],board_weight[queue_empty[0]]]
                        for q in queue_empty:
                            if board_weight[q]>best[1]:
                                best=[q,board_weight[q]]
                        self.orders.append(potocole.encodeOrder(best[0],nid,AMOUNT_PROTECT))
                    elif len(queue_provide)>=1:
                        if len(queue_provide)==1:
                            self.orders.append(potocole.encodeOrder(queue_provide[0],nid,AMOUNT_PROTECT))
                        else:
                            best=[queue_provide[0],board_weight[queue_provide[0]]]
                            for q in queue_provide:
                                if board_weight[q]>best[1]:
                                    best=[q,board_weight[q]]
                            self.orders.append(potocole.encodeOrder(best[0],nid,AMOUNT_PROTECT))
                    elif len(queue_osef)>=1:
                        if len(queue_osef)==1:
                            self.orders.append(potocole.encodeOrder(queue_osef[0],nid,AMOUNT_PROTECT))
                        else:
                            best=[queue_osef[0],board_weight[queue_osef[0]]]
                            for q in queue_osef:
                                if board_weight[q]>best[1]:
                                    best=[q,board_weight[q]]
                            self.orders.append(potocole.encodeOrder(best[0],nid,AMOUNT_PROTECT))

                if order=="conquer":
                    if len(queue_empty)>=1:
                        if len(queue_empty)==1:
                            self.orders.append(potocole.encodeOrder(queue_empty[0],nid,AMOUNT_CONQUER))
                        else:
                            best=[queue_empty[0],board_weight[queue_empty[0]]]
                            for q in queue_empty:
                                if board_weight[q]>best[1]:
                                    best=[q,board_weight[q]]
                            self.orders.append(potocole.encodeOrder(best[0],nid,AMOUNT_CONQUER))
                    elif len(queue_provide)>=1:
                        if len(queue_provide)==1:
                            self.orders.append(potocole.encodeOrder(queue_provide[0],nid,AMOUNT_CONQUER))
                        else:
                            best=[queue_provide[0],board_weight[queue_provide[0]]]
                            for q in queue_provide:
                                if board_weight[q]>best[1]:
                                    best=[q,board_weight[q]]
                            self.orders.append(potocole.encodeOrder(best[0],nid,AMOUNT_CONQUER))
                    elif len(queue_osef)>=1:
                        if len(queue_osef)==1:
                            self.orders.append(potocole.encodeOrder(queue_osef[0],nid,AMOUNT_CONQUER))
                        else:
                            best=[queue_osef[0],board_weight[queue_osef[0]]]
                            for q in queue_osef:
                                if board_weight[q]>best[1]:
                                    best=[q,board_weight[q]]
                            self.orders.append(potocole.encodeOrder(best[0],nid,AMOUNT_CONQUER))
                
                if order=="attack":
                    if len(queue_empty)>=1:
                        if len(queue_empty)==1:
                            self.orders.append(potocole.encodeOrder(queue_empty[0],nid,AMOUNT_ATTACK))
                        else:
                            best=[queue_empty[0],board_weight[queue_empty[0]]]
                            for q in queue_empty:
                                if board_weight[q]>best[1]:
                                    best=[q,board_weight[q]]
                            self.orders.append(potocole.encodeOrder(best[0],nid,AMOUNT_ATTACK))
                    elif len(queue_provide)>=1:
                        if len(queue_provide)==1:
                            self.orders.append(potocole.encodeOrder(queue_provide[0],nid,AMOUNT_ATTACK))
                        else:
                            best=[queue_provide[0],board_weight[queue_provide[0]]]
                            for q in queue_provide:
                                if board_weight[q]>best[1]:
                                    best=[q,board_weight[q]]
                            self.orders.append(potocole.encodeOrder(best[0],nid,AMOUNT_ATTACK))
                            
                if order=="provide":
                    if len(queue_empty)>=1:
                        if len(queue_empty)==1:
                            self.orders.append(potocole.encodeOrder(queue_empty[0],nid,AMOUNT_PROVIDE))
                        else:
                            best=[queue_empty[0],board_weight[queue_empty[0]]]
                            for q in queue_empty:
                                if board_weight[q]>best[1]:
                                    best=[q,board_weight[q]]
                            self.orders.append(potocole.encodeOrder(best[0],nid,AMOUNT_PROVIDE))    
                    elif len(queue_osef)>=1:
                        if len(queue_osef)==1:
                            self.orders.append(potocole.encodeOrder(queue_osef[0],nid,AMOUNT_PROVIDE))
                        else:
                            best=[queue_osef[0],board_weight[queue_osef[0]]]
                            for q in queue_osef:
                                if board_weight[q]>best[1]:
                                    best=[q,board_weight[q]]
                            self.orders.append(potocole.encodeOrder(best[0],nid,AMOUNT_PROVIDE))
                            
    def strat_relevance(self):
        # STRATEGIE RELEVANCE (seulement les poids)
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
        nodes_to_empty_emergency=[]
        for n in own_nodes:
            relevance=(board_weight[n.id]-minw)/ecart
            if n.units >= 10+10*n.productionSpeed - 1 : # si on garde les unites ici, on perdra des unites !!!
                nodes_to_empty_emergency.append(n);
                print("NODE"+str(n.id)+" TO EMPTY EMERGENCY")
            elif relevance<RELEVANCE_MIN:
                        nodes_to_empty.append(n)
                        print("NODE"+str(n.id)+" TO EMPTY")
            
        # Dispatch + Elimination des nodes peu importants (Relevance < x%)
        for n in nodes_to_empty_emergency :
            noeuds_potes = n.getAdjoining() ;
            #on l'envoie vers l'ennemi ! Yaaar !
            for n_p in noeuds_potes :
                if n_p.owner != n.owner :
                    self.orders.append(potocole.encodeOrder(n.id,n_p.id,90));
                    break;
            else : #il n'y a que des allies autour ... donc on essaye de tempo pour pas avoir de pertes !
                valeur_max = None ;
                node_max = None ;
                for node_friend in noeuds_potes :
                    if valeur_max is None :
                        node_max = node_friend ;
                        valeur_max = (board_weight[node_friend.id]-minw)/ecart ;
                    elif valeur_max < (board_weight[node_friend.id]-minw)/ecart :
                        node_max = node_friend ;
                        valeur_max = (board_weight[node_friend.id]-minw)/ecart ;
                print("EMERGENCY : SEND "+str(n.id)+" TO "+str(node_max.id));
                self.orders.append(potocole.encodeOrder(n.id,node_max.id,30));
                
                    
                    
            
        for n in nodes_to_explore:
                    print("EXPLORING DESTINATION NODE"+str(n.id))
                    relevance=(board_weight[n.id]-minw)/ecart
                    print("RELEVANCE :"+str(relevance));
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
        
        
        adjoining = node.getAdjoining()
        number_allies_adj=0
        for obj in adjoining :
                    if obj.owner == owner :
                        number_allies_adj+=1
                        if node.owner == owner or node.owner == -1 :
                            sum += WEIGHT_ALLIES + WEIGHT_RATIO_PRODUCTION* (obj.productionSpeed-1) ;
                        else:
                            sum -= WEIGHT_ALLIES *(1+WEIGHT_PER_UNIT*node.units)
                    elif obj.owner == -1 :
                        sum += WEIGHT_NEUTRAL + WEIGHT_RATIO_PRODUCTION* (obj.productionSpeed-1);
                    else :
                        if node.owner == owner or node.owner == -1 :
                            sum += WEIGHT_ENEMIES *(1+WEIGHT_PER_UNIT*node.units) + WEIGHT_RATIO_PRODUCTION* (obj.productionSpeed-1)  ;
                        else :
                            sum -= WEIGHT_ENEMIES *(1+WEIGHT_PER_UNIT*obj.units) ;
                            
        if number_allies_adj==len(adjoining):
            sum+=WEIGHT_SURROUNDED_BY_ALLIES
        if number_allies_adj==len(adjoining)-1:
            sum+=WEIGHT_ONE_TARGET
        return sum ;
        
        
