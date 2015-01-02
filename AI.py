from board import Board

class AI:
    def __init__(self,board):
        self.board = board ;
        
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
        
    def getBestOrder(self,playerNb):
        pass
    
    def evalBoardByNodeWeight(self,playerNb):
        for n in self.board.nodes:
            print(str(n.id)+" : "+str(self.evalNodeWeight(n,playerNb)))

    def evalNodeWeight(self,node,owner):
        sum =0
        
        WEIGHT_SELF_ALLY=2; # superieur a WEIGHT SELF ENEMY: tendence à la defense, sinon YOLO
        WEIGHT_SELF_ENEMY=6; # superieur a WEIGHT SELF ALLY : tendence à l'attaque
        WEIGHT_ALLIES=-2;
        WEIGHT_NEUTRAL=2;
        WEIGHT_ENEMIES=4;
        WEIGHT_RATIO_PRODUCTION=3;
        WEIGHT_PER_UNIT = 0.2 ;
        
        if (owner == node.owner):
            sum+=WEIGHT_SELF_ALLY ;
        else :
            sum+=WEIGHT_SELF_ENEMY*(1+WEIGHT_PER_UNIT*node.units) ;
        
        #TODO : 5 et 6 bugue pour joueur 3 !!!!!
        adjoining = node.getAdjoining()
        for obj in adjoining :
            if obj.owner == owner :
                if node.owner == owner or node.owner == -1 :
                    sum += WEIGHT_ALLIES + WEIGHT_RATIO_PRODUCTION* (1-obj.productionSpeed) ;
                else:
                    sum -= WEIGHT_ALLIES *(1+WEIGHT_PER_UNIT*obj.units)
            elif obj.owner == 0 :
                sum += WEIGHT_NEUTRAL + WEIGHT_RATIO_PRODUCTION* (1-obj.productionSpeed)  ;
            else :
                if node.owner == owner or node.owner == -1 :
                    sum += WEIGHT_ENEMIES *(1+WEIGHT_PER_UNIT*obj.units) + WEIGHT_RATIO_PRODUCTION* (1-obj.productionSpeed)  ;
                else :
                    sum -= WEIGHT_ENEMIES *(1+WEIGHT_PER_UNIT*obj.units) ;
                    
        return sum ;
        
        
