from typing import List, Dict, Tuple
import random
import numpy as np

class Node:

    def __init__(self, 
                 id,
                 type:str, 
                 state:np.array, 
                 value=None,
                 terminal=False,
                 ) -> None:
        
        self.type = type
        self.state = state
        self.value = value
        self.children = {}
        self.id = id
        self.terminal = terminal

    def add_child(self, action, node):
        self.children[action] = node
    
    def get_max_action(self):
        values = []
        actions = []
        for action, child in self.children.items():
            val = child.value
            values.append(val)
            actions.append(action)
        
        max_index = np.argmax(values)

        return actions[max_index]


