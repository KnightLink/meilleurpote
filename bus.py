import edge.py
import node.py

class Bus: # Vaisseau de transport d'unités
    def __init__(self,owner,direction,units,progress):
        self.owner=owner
        self.direction=direction
        self.units=units
        self.progress=progress