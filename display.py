from tkinter import *
from tkinter import ttk
from board import *

class Display(Frame):
    def __init__(self, board, master=None, canvas=None):
        Frame.__init__(self, master)
        self.board=board
        self.canvas=canvas

    def full_display(self,mult_padding=0.025,add_padding=30,mult_size=0.2):
        
        self.nodes_display(mult_padding,add_padding,mult_size)
        self.edges_display(mult_padding,add_padding,mult_size)
        self.moves_display(mult_padding,add_padding,mult_size)

    def moves_display(self,mult_padding,add_padding,mult_size):
        for n in self.board.nodes :
            
            for edge in n.edges :
                for bus in edge.bus :
                    if bus.owner==-1:
                        cfill="grey"
                    if bus.owner==0:
                        cfill="red"
                    if bus.owner==1:
                        cfill="blue"
                    if bus.owner==2:
                        cfill="green"
                    if bus.owner==3:
                        cfill="yellow"
                    progress=((self.board.time-bus.time_start)/edge.length)*2
                    if bus.destination==edge.node2.id:
                        self.canvas.create_oval(edge.node1.x*mult_padding+add_padding+edge.node1.r*mult_size/2+((edge.node2.x*mult_padding+add_padding+edge.node2.r*mult_size/2)-(edge.node1.x*mult_padding+add_padding+edge.node1.r*mult_size/2))*progress-3,
                                                edge.node1.y*mult_padding+add_padding+edge.node1.r*mult_size/2+((edge.node2.y*mult_padding+add_padding+edge.node2.r*mult_size/2)-(edge.node1.y*mult_padding+add_padding+edge.node1.r*mult_size/2))*progress-3,
                                                edge.node1.x*mult_padding+add_padding+edge.node1.r*mult_size/2+((edge.node2.x*mult_padding+add_padding+edge.node2.r*mult_size/2)-(edge.node1.x*mult_padding+add_padding+edge.node1.r*mult_size/2))*progress+3,
                                                edge.node1.y*mult_padding+add_padding+edge.node1.r*mult_size/2+((edge.node2.y*mult_padding+add_padding+edge.node2.r*mult_size/2)-(edge.node1.y*mult_padding+add_padding+edge.node1.r*mult_size/2))*progress+3,fill=cfill)
                        self.canvas.create_text(edge.node1.x*mult_padding+add_padding+edge.node1.r*mult_size/2+((edge.node2.x*mult_padding+add_padding+edge.node2.r*mult_size/2)-(edge.node1.x*mult_padding+add_padding+edge.node1.r*mult_size/2))*progress-2,
                                                edge.node1.y*mult_padding+add_padding+edge.node1.r*mult_size/2+((edge.node2.y*mult_padding+add_padding+edge.node2.r*mult_size/2)-(edge.node1.y*mult_padding+add_padding+edge.node1.r*mult_size/2))*progress-10,text=bus.units)
                    else:
                        self.canvas.create_oval(edge.node2.x*mult_padding+add_padding+edge.node2.r*mult_size/2+((edge.node1.x*mult_padding+add_padding+edge.node1.r*mult_size/2)-(edge.node2.x*mult_padding+add_padding+edge.node2.r*mult_size/2))*progress-3,
                                                edge.node2.y*mult_padding+add_padding+edge.node2.r*mult_size/2+((edge.node1.y*mult_padding+add_padding+edge.node1.r*mult_size/2)-(edge.node2.y*mult_padding+add_padding+edge.node2.r*mult_size/2))*progress-3,
                                                edge.node2.x*mult_padding+add_padding+edge.node2.r*mult_size/2+((edge.node1.x*mult_padding+add_padding+edge.node1.r*mult_size/2)-(edge.node2.x*mult_padding+add_padding+edge.node2.r*mult_size/2))*progress+3,
                                                edge.node2.y*mult_padding+add_padding+edge.node2.r*mult_size/2+((edge.node1.y*mult_padding+add_padding+edge.node1.r*mult_size/2)-(edge.node2.y*mult_padding+add_padding+edge.node2.r*mult_size/2))*progress+3,fill=cfill)
                        self.canvas.create_text(edge.node2.x*mult_padding+add_padding+edge.node2.r*mult_size/2+((edge.node1.x*mult_padding+add_padding+edge.node1.r*mult_size/2)-(edge.node2.x*mult_padding+add_padding+edge.node2.r*mult_size/2))*progress-2,
                                                edge.node2.y*mult_padding+add_padding+edge.node2.r*mult_size/2+((edge.node1.y*mult_padding+add_padding+edge.node1.r*mult_size/2)-(edge.node2.y*mult_padding+add_padding+edge.node2.r*mult_size/2))*progress-10,text=bus.units)

    def nodes_display(self,mult_padding,add_padding,mult_size):
        for node in self.board.nodes:
            if node.owner==-1:
                cfill="grey"
            if node.owner==0:
                cfill="red"
            if node.owner==1:
                cfill="blue"
            if node.owner==2:
                cfill="green"
            if node.owner==3:
                cfill="yellow"
            self.canvas.create_oval(node.x*mult_padding+add_padding,node.y*mult_padding+add_padding,node.x*mult_padding+node.r*mult_size+add_padding,node.y*mult_padding+node.r*mult_size+add_padding,fill=cfill)
            self.canvas.create_text(node.x*mult_padding+add_padding,node.y*mult_padding+add_padding-10,text=node.units,fill="black")

    def edges_display(self,mult_padding,add_padding,mult_size):
        for n in self.board.nodes :
            for edge in n.edges :
                self.canvas.create_line(edge.node1.x*mult_padding+add_padding+edge.node1.r*mult_size/2,
                                        edge.node1.y*mult_padding+add_padding+edge.node1.r*mult_size/2,
                                        edge.node2.x*mult_padding+add_padding+edge.node2.r*mult_size/2,
                                        edge.node2.y*mult_padding+add_padding+edge.node2.r*mult_size/2)
                    
		
