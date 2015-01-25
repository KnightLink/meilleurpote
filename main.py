import re
from board import *
from AI import AI
import potocole
from display import *
from tkinter import *
from tkinter import ttk

mainBoard=Board(3,[
{'nbUnits':10,'owner':0},
{'nbUnits':15,'owner':0},
{'nbUnits':15,'owner':0},
{'nbUnits':10,'owner':1,'speed':3},
{'nbUnits':20,'owner':1},
{'nbUnits':20,'owner':1},
{'nbUnits':25,'owner':2},
{'nbUnits':20,'owner':2},
{'nbUnits':5,'owner':1},
{'nbUnits':5,'owner':0}
])
mainBoard.addEdges([
(0,1,2000),
(0,2,2000),
(3,4,2000),
(3,5,2000),
(6,7,2000),
(6,8,2000),
(1,9,3000),
(3,9,3000),
(4,9,3000),
(5,9,3000),
(7,9,3000),
(8,9,3000)]);

ai=AI(mainBoard);
print(mainBoard);

print(ai.evalBoard(0))
print(ai.evalBoard(1))
print(ai.evalBoard(2))

print(ai.evalBoardByNodeWeight(1,True))

root=Tk()
root.title="Test"
app=Display(mainBoard,master=root)
app.mainloop()
root.destroy()
