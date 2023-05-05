
from tkinter import *
import numpy as np
import random
# from tree import RandPlayer
from game import Tic_Tac_Toe, RandPlayer, SmartPlayer
from main import think, minmax

id2node = {}
print('Starting to think')
root_node = think()
print('Finished thinking. Now determining values')
minmax(root_node, id2node)
print('Done with the thinkg. Let"s play')

player1 = SmartPlayer(id2node)

start_player='max'
game_instance = Tic_Tac_Toe(X='max', O='min', 
                            ai=player1,
                              starter=start_player,
                              title='AI Tic Toc Player')
game_instance.mainloop()
