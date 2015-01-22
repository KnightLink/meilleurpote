import re
from board import *
from AI import AI
import potocole

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
(1,2,2000),
(1,3,2000),
(4,5,2000),
(4,6,2000),
(7,8,2000),
(7,9,2000),
(2,10,3000),
(3,10,3000),
(5,10,3000),
(6,10,3000),
(8,10,3000),
(9,10,3000)]);

ai=AI(mainBoard);
print(mainBoard);

print(ai.evalBoard(0))
print(ai.evalBoard(1))
print(ai.evalBoard(2))

print(ai.evalBoardByNodeWeight(1))
