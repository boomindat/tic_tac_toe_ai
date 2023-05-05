# Author: aqeelanwar
# Created: 12 March,2020, 7:06 PM
# Email: aqeel.anwar@gatech.edu

from tkinter import *
from game import Tic_Tac_Toe, RandPlayer, SmartPlayer
from main import think, minmax

id2node = {}
print('Starting to think')
root_node = think()
print('Finished thinking. Now determining values')
minmax(root_node, id2node)
print('Done with the thinkg. Let"s play')

player1 = SmartPlayer(id2node)

# player1 = RandPlayer()
player2 = RandPlayer()

start_player='max'
game_instance = Tic_Tac_Toe(X='max', O='min', ai=player1, starter=start_player)

n_games = 10000
next_state = game_instance.board_status
next_player = start_player

scores = {'min':0, 'max':0, 'tie': 0}
for i in range(n_games):
    while True:
        actions = game_instance.possible_moves(next_state)
        # print(next_player, state_to_id(next_state))
        if next_player == 'max':
            action = player1('max', next_state, actions)
        else:
            action = player2('min', next_state, actions)
        x, y = action
        prev_player = next_player
        next_state, next_player, is_over, utility = game_instance.simulate_play(next_state, 
                                                                                next_player, x, y)
        # print(x, y, next_player, state_to_id(next_state))
        if is_over:
            if utility == 1:
                scores[prev_player] += 1
            else:
                scores['tie'] += 1
            next_player = start_player
            next_state = game_instance.reset_game_state(starter=start_player)
            break

min_win = scores['min'] * 100 / n_games
max_win = scores['max']  * 100/ n_games
tie = scores['tie']  * 100 / n_games
print(f'Min: {min_win}%, Max: {max_win}%, Tie: {tie}%')