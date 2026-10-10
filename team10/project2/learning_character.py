# This is necessary to find the main code
import sys
import time
import math
import json
import os
sys.path.insert(0, '../bomberman')
# Import necessary stuff
from entity import CharacterEntity
from colorama import Fore, Back
from sensed_world import SensedWorld
from events import Event
# import A_star
import state_functions

# File where the weights are stored between simulations
WEIGHTS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "weights.json")

class LearningCharacter(CharacterEntity):
    def __init__(self, name, avatar, x, y, new_weights = [-58.0, 42.7, 3.3, -18.4, -30, -30], weights_file = WEIGHTS_FILE):
        super().__init__(name, avatar, x, y)
        self.total_moves = 0
        self.previous_position = (x, y)
        self.weights_file = weights_file
        #self.weights is the list of weights used in Approximate Q-Learning
        #Distance to monster, distance to exit, distance to explosion, in bomb radius
        self.weights = self.load_weights(new_weights)
        
        self.learning_rate = 0.05
        self.gamma = 0.9

    # Get the weights from the file
    def load_weights(self, default):
        try:
            with open(self.weights_file) as f:
                saved = json.load(f)
            if isinstance(saved, list) and len(saved) == len(default):
                return saved
        except (FileNotFoundError, json.JSONDecodeError):
            pass
        return list(default)

    # Save weights to the file
    def save_weights(self):
        tmp = self.weights_file + ".tmp"
        with open(tmp, "w") as f:
            json.dump(self.weights, f)
        os.replace(tmp, self.weights_file)
    
    def count_move(self):
        #If the character moves, increment the total moves of the character
        position = (self.x, self.y)
        if position != self.previous_position:
            self.total_moves += 1
            self.previous_position = position

    def done(self, wrld):
        #Counts the moves done by the character
        self.count_move()
        # If you want to train weights between simulations, uncomment line below
        # self.save_weights()
        print("Final weights:", self.weights)
        print("Final total moves:", self.total_moves)

    def get_Q_value(self, wrld):
        me = wrld.me(self)

        if me is None or wrld.time <= 0:
            return 0

        #Sums values to create Q-value
        value = 0
        function_values = state_functions.get_function_values(me, wrld)
        for i in range(len(self.weights)):
            print(function_values[i])
            value += self.weights[i] * function_values[i]
        return value

    def do(self, wrld):
        self.count_move()
        self.move(0, 0)

        q_val = self.get_Q_value(wrld)

        max_value = -math.inf
        best_move = None

        for action in state_functions.get_valid_actions(self, wrld):
            #Only use a bomb if you are vertically/horizontally adjacent to a wall
            if action == "b" and not (state_functions.near_wall(self, wrld) or (state_functions.monster_distance_function(self, wrld) != 0)):
                continue

            sim = SensedWorld.from_world(wrld)
            me = sim.me(self)
            me.move(0,0)

            if action == "b":
                me.place_bomb()
            elif action != "n":
                me.move(*action)

            next_world, _ = sim.next()

            reward = state_functions.give_custom_score(self, next_world)
            if action == "b":
                reward += 0.5
            new_Q = self.get_Q_value(next_world)
            value = reward + self.gamma * new_Q

            if value > max_value:
                best_move = action
                max_value = value
            print("Action:", action, "Value:", value)

        # Updates each weight
        error = max_value - q_val
        weights = state_functions.get_function_values(self, wrld)
        for i in range(len(self.weights)):
            self.weights[i] += self.learning_rate * error * weights[i]
        print("Weights:", self.weights)

        if best_move == "b":
            self.place_bomb()
        elif best_move != "n" and best_move is not None:
            dx, dy = best_move
            self.move(dx, dy)

        print("Best move:", best_move)

