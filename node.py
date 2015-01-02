import edge

class Node: # Noeud
    def __init__(self,id,owner=0,production_speed=1):
        self.id=id
        self.edges=[]
        self.owner=owner # 0 = neutre
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
        
    def evalWeight(self,owner):
        sum =0
        
        WEIGHT_SELF_ALLY=2; # superieur a WEIGHT SELF ENEMY: tendence à la defense, sinon YOLO
        WEIGHT_SELF_ENEMY=6; # superieur a WEIGHT SELF ALLY : tendence à l'attaque
        WEIGHT_ALLIES=-2;
        WEIGHT_NEUTRAL=2;
        WEIGHT_ENEMIES=4;
        WEIGHT_RATIO_PRODUCTION=3;
        WEIGHT_PER_UNIT = 0.2 ;
        
        if (owner == self.owner):
            sum+=WEIGHT_SELF_ALLY ;
        else :
            sum+=WEIGHT_SELF_ENEMY*(1+WEIGHT_PER_UNIT*self.units) ;
        
        #TODO : 5 et 6 bugue pour joueur 3 !!!!!
        adjoining = self.getAdjoining()
        for obj in adjoining :
            if obj.owner == owner :
                if self.owner == owner or self.owner == 0 :
                    sum += WEIGHT_ALLIES + WEIGHT_RATIO_PRODUCTION* (1-obj.productionSpeed) ;
                else:
                    sum -= WEIGHT_ALLIES *(1+WEIGHT_PER_UNIT*obj.units)
            elif obj.owner == 0 :
                sum += WEIGHT_NEUTRAL + WEIGHT_RATIO_PRODUCTION* (1-obj.productionSpeed)  ;
            else :
                if self.owner == owner or self.owner == 0 :
                    sum += WEIGHT_ENEMIES *(1+WEIGHT_PER_UNIT*obj.units) + WEIGHT_RATIO_PRODUCTION* (1-obj.productionSpeed)  ;
                else :
                    sum -= WEIGHT_ENEMIES *(1+WEIGHT_PER_UNIT*obj.units) ;
                    
        return sum ;
                
        