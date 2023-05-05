

# Build a tree for the game
    # write a small library of tree
    # Write DFS to build the tree
# determine the values of the nodes
    # we will use Recursion to determine values
    # use this tree to play
# Build a state-action pair
    # everytime we make a decision, use the the state-action pair

from game import Tic_Tac_Toe, RandPlayer, state_to_id
from tree import Node
import numpy as np

def think():
    player1 = RandPlayer()

    start_player = 'max'
    game = Tic_Tac_Toe(X='max', O='min', ai=player1, starter=start_player)

    next_player = start_player
    next_state = game.board_status
    id = next_player + "," + state_to_id(next_state)
    root_node = Node(id=id,
                    type=next_player,
                    state=next_state,
                    value=None,
                    terminal=False
                    )

    Q = [root_node]
    while len(Q) > 0:

        parent = Q.pop()
        if parent.terminal:
            continue
        actions = game.possible_moves(parent.state)
        for action in actions:
            new_state, next_player, is_over, utility = game.simulate_play(state=parent.state, 
                                                                    player=parent.type,
                                                                        x=action[0], y=action[1])
            if is_over:
                terminal = True
                value = utility
            else:
                terminal = False
                value = None
            
            id = next_player + "," + state_to_id(new_state)
            child_node = Node(id=id,
                    type=next_player,
                    state=new_state,
                    value=value,
                    terminal=terminal
                    )
            parent.add_child(action=action, node=child_node)
            Q.append(child_node)

    return root_node

def minmax(root_node: Node, id2node: dict):
    id2node[root_node.id] = root_node
    if root_node.terminal:
        if root_node.type == 'max':
            return root_node.value
        else:
            if root_node.value == 1: # if player was MIN and He won
                return -1
        
        return root_node.value # 0
    
    else:
        if root_node.type == 'max':
            values = []

            for action, child in root_node.children.items():
                val = minmax(child, id2node)
                values.append(val)
            
            max_index = np.argmax(values)
            max_val = values[max_index]
            root_node.value = max_val
            return max_val

        else:
            values = []
            
            for action, child in root_node.children.items():
                val = minmax(child, id2node)
                values.append(val)
            
            min_index = np.argmin(values)
            min_val = values[min_index]
            root_node.value = min_val
            return min_val



# print("finished")

