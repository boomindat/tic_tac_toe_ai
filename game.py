
from tkinter import *
import numpy as np
import random

size_of_board = 600
symbol_size = (size_of_board / 3 - size_of_board / 8) / 2
symbol_thickness = 50
symbol_X_color = '#EE4035'
symbol_O_color = '#0492CF'
Green_color = '#7BC043'
import time


class Tic_Tac_Toe():
    # ------------------------------------------------------------------
    # Initialization Functions:
    # ------------------------------------------------------------------
    def __init__(self, ai, X='max', O='min', starter='max', title='game'):
        self.window = Tk()
        self.window.title(title)
        self.starter = starter
        self.frame_a = Frame(self.window, width=size_of_board, height=size_of_board)
        self.frame_b = Frame(self.window, width=100, height=100)
        self.canvas = Canvas(self.frame_a, width=size_of_board, height=size_of_board)
        self.canvas.pack()
        self.button = Button(
            master=self.frame_b,
                text="AI Play",
                width=25,
                height=5,
            )
        self.button.pack()
        self.frame_a.pack()
        self.frame_b.pack()
        self.X = X
        self.O = O
        self.ai = ai
        # Input from user in form of clicks
        self.canvas.bind('<Button-1>', self.click)
        self.button.bind("<Button-1>", self.ai_play)

        self.initialize_board()
        self.player_X_turns = X == starter
        self.board_status = np.zeros(shape=(3, 3), dtype=np.int32)

        self.player_X_starts = X == starter
        self.reset_board = False
        self.gameover = False
        self.tie = False
        self.X_wins = False
        self.O_wins = False

        self.X_score = 0
        self.O_score = 0
        self.tie_score = 0

    def mainloop(self):
        self.window.mainloop()
    

    def initialize_board(self):
        for i in range(2):
            self.canvas.create_line((i + 1) * size_of_board / 3, 0, (i + 1) * size_of_board / 3, size_of_board)

        for i in range(2):
            self.canvas.create_line(0, (i + 1) * size_of_board / 3, size_of_board, (i + 1) * size_of_board / 3)

    def play_again(self):
        self.initialize_board()
        self.player_X_starts = self.X == self.starter
        self.board_status = np.zeros(shape=(3, 3), dtype=np.int32)

    def reset_game_state(self, starter):
        self.player_X_starts = self.X == starter
        self.player_X_turns = self.X == starter
        self.board_status = np.zeros(shape=(3, 3), dtype=np.int32)
        return self.board_status
    # ------------------------------------------------------------------
    # Drawing Functions:
    # The modules required to draw required game based object on canvas
    # ------------------------------------------------------------------

    def draw_O(self, logical_position):
        logical_position = np.array(logical_position)
        # logical_position = grid value on the board
        # grid_position = actual pixel values of the center of the grid
        grid_position = self.convert_logical_to_grid_position(logical_position)
        self.canvas.create_oval(grid_position[0] - symbol_size, grid_position[1] - symbol_size,
                                grid_position[0] + symbol_size, grid_position[1] + symbol_size, width=symbol_thickness,
                                outline=symbol_O_color)

    def draw_X(self, logical_position):
        grid_position = self.convert_logical_to_grid_position(logical_position)
        self.canvas.create_line(grid_position[0] - symbol_size, grid_position[1] - symbol_size,
                                grid_position[0] + symbol_size, grid_position[1] + symbol_size, width=symbol_thickness,
                                fill=symbol_X_color)
        self.canvas.create_line(grid_position[0] - symbol_size, grid_position[1] + symbol_size,
                                grid_position[0] + symbol_size, grid_position[1] - symbol_size, width=symbol_thickness,
                                fill=symbol_X_color)

    def display_gameover(self):

        if self.X_wins:
            self.X_score += 1
            text = 'Winner: Player 1 (X)'
            color = symbol_X_color
        elif self.O_wins:
            self.O_score += 1
            text = 'Winner: Player 2 (O)'
            color = symbol_O_color
        else:
            self.tie_score += 1
            text = 'Its a tie'
            color = 'gray'

        self.canvas.delete("all")
        self.canvas.create_text(size_of_board / 2, size_of_board / 3, font="cmr 60 bold", fill=color, text=text)

        score_text = 'Scores \n'
        self.canvas.create_text(size_of_board / 2, 5 * size_of_board / 8, font="cmr 40 bold", fill=Green_color,
                                text=score_text)

        score_text = 'Player 1 (X) : ' + str(self.X_score) + '\n'
        score_text += 'Player 2 (O): ' + str(self.O_score) + '\n'
        score_text += 'Tie                    : ' + str(self.tie_score)
        self.canvas.create_text(size_of_board / 2, 3 * size_of_board / 4, font="cmr 30 bold", fill=Green_color,
                                text=score_text)
        self.reset_board = True

        score_text = 'Click to play again \n'
        self.canvas.create_text(size_of_board / 2, 15 * size_of_board / 16, font="cmr 20 bold", fill="gray",
                                text=score_text)

    # ------------------------------------------------------------------
    # Logical Functions:
    # The modules required to carry out game logic
    # ------------------------------------------------------------------

    def convert_logical_to_grid_position(self, logical_position):
        logical_position = np.array(logical_position, dtype=int)
        return (size_of_board / 3) * logical_position + size_of_board / 6

    def convert_grid_to_logical_position(self, grid_position):
        grid_position = np.array(grid_position)
        return np.array(grid_position // (size_of_board / 3), dtype=int)

    def is_grid_occupied(self, logical_position):
        if self.board_status[logical_position[0]][logical_position[1]] == 0:
            return False
        else:
            return True

    def is_winner(self, state, player):

        player = -1 if player == self.X else 1

        # Three in a row
        for i in range(3):
            if state[i][0] == state[i][1] == state[i][2] == player:
                return True
            if state[0][i] == state[1][i] == state[2][i] == player:
                return True

        # Diagonals
        if state[0][0] == state[1][1] == state[2][2] == player:
            return True

        if state[0][2] == state[1][1] == state[2][0] == player:
            return True

        return False
    

    def is_tie(self, state):

        r, c = np.where(state == 0)
        # print(np.where(state == 0))
        tie = False
        if len(r) == 0:
            tie = True

        return tie


    def is_gameover(self, state):
        # Either someone wins or all grid occupied
        self.X_wins = self.is_winner(state, self.X)
        if not self.X_wins:
            self.O_wins = self.is_winner(state, self.O)

        if not self.O_wins:
            self.tie = self.is_tie(state)
            # print(self.tie)
        gameover = self.X_wins or self.O_wins or self.tie

        winner = None
        if self.X_wins:
            # print('X wins')
            winner = 'X'
        if self.O_wins:
            # print('O wins')
            winner = 'O'
        if self.tie:
            # print('Its a tie')
            winner = 'T'

        return gameover, winner

    def possible_moves(self, state):
        open_moves = []
        for i in range(len(state)):
            for j in range(len(state[0])):
                if state[i][j] == 0:
                    open_moves.append((i, j))
        return open_moves
    
    def simulate_play(self, state, player, x, y):
        new_state = np.copy(state)
        if player == self.X:
            next_player = self.O
            new_state[x][y] = -1
        else:
            next_player = self.X
            new_state[x][y] = 1

        self.player_X_turns = not self.player_X_turns
        
        win = self.is_winner(new_state, player)
        is_over, winner = self.is_gameover(new_state)
        # print(is_over, winner)
        utility = None
        if is_over and winner != 'T':
            utility = 1
        elif is_over and winner == 'T':
            utility = 0
        
        return new_state, next_player, is_over, utility

    def click(self, event):
        grid_position = [event.x, event.y]
        logical_position = self.convert_grid_to_logical_position(grid_position)

        if not self.reset_board:
            if not self.player_X_turns:
                if not self.is_grid_occupied(logical_position):
                    self.draw_O(logical_position)
                    self.board_status[logical_position[0]][logical_position[1]] = 1
                    self.player_X_turns = not self.player_X_turns

            # Check if game is concluded
            is_over, winner = self.is_gameover(self.board_status)
            if is_over:
                self.canvas.update()
                time.sleep(1)
                self.display_gameover()
                # print('Done')
        else:  # Play Again
            self.canvas.delete("all")
            self.play_again()
            self.reset_board = False

    def ai_play(self, event):

        # logical_position = self.convert_grid_to_logical_position(grid_position)
        actions = self.possible_moves(self.board_status)
        action = self.ai('max', self.board_status, actions)
        if not self.reset_board:
            if self.player_X_turns:
                if not self.is_grid_occupied(action):
                    self.draw_X(action)
                    self.board_status[action[0]][action[1]] = -1
                    self.player_X_turns = not self.player_X_turns

            # Check if game is concluded
            is_over, winner = self.is_gameover(self.board_status)
            if is_over:
                self.canvas.update()
                time.sleep(1)
                self.display_gameover()



class RandPlayer:

    def __call__(self, type, state,  actions):
        r = random.randint(0, len(actions) - 1)
        return actions[r]
    
class SmartPlayer:

    def __init__(self, id2node) -> None:
        self.id2node = id2node

    def __call__(self, type, state,  actions):
        id = type + "," + state_to_id(state)
        node = self.id2node[id]
        action = node.get_max_action()
        return action
    
    
def get_next_player(player):
    if player == 'max':
        return 'min'
    return 'max'

def state_to_id(state):
    id = ",".join([str(x) for x in state.flatten()])
    return id

def id_to_state(id):
    return np.array([int(x) for x in id.split(',')], dtype=np.int32).reshape((3, 3))
