from tkinter import *
from tkinter import ttk
from board import *

class Display(Frame):
    def __init__(self, board, master=None):
        Frame.__init__(self, master)
        self.board=board
    