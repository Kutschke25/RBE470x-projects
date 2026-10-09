# This is necessary to find the main code
import sys
import time
import math
sys.path.insert(0, '../bomberman')
# Import necessary stuff
from entity import CharacterEntity
from colorama import Fore, Back
from sensed_world import SensedWorld
from events import Event
# import A_star
import state_functions


class LearnedCharacter(CharacterEntity):
    def __init__(self, name, avatar, x, y):
        super().__init__(name, avatar, x, y)
        self.total_moves = 0
        self.previous_position = (x, y)
        #self.weights is the list of weights used in Approximate Q-Learning
        #monster distance (euclidian), exit distance, explosian distance, in bomb radius, monster chasing, monster distance (chebyshev)
        self.weights = [-34.71315543021304, 105.06110350366828, -0.833717060692577, -25.10737029677307, -21.13346151214482, -13.491068851225133]
        self.gamma = 0.9

    def count_move(self):
        #If the character moves, increment the total moves of the character
        position = (self.x, self.y)
        if position != self.previous_position:
            self.total_moves += 1
            self.previous_position = position

    def done(self, wrld):
        #Counts the moves done by the character
        self.count_move()
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
            if action == "b":
                #Only use a bomb if you are vertically/horizontally adjacent to a wall
                if not state_functions.near_wall(self, wrld):
                    continue

            me = wrld.me(self)

            if action == "b":
                me.place_bomb()
            elif action != "n":
                dx, dy = action
                me.move(dx, dy)

            next_world, _ = wrld.next()

            reward = state_functions.give_custom_score(self, next_world)
            if action == "b":
                reward += 2
            new_Q = self.get_Q_value(next_world)
            value = reward + self.gamma * new_Q

            if value > max_value:
                best_move = action
                max_value = value
            print("Action:", action, "Value:", value)

        if best_move == "b":
            self.place_bomb()
        elif best_move != "n" and best_move is not None:
            dx, dy = best_move
            self.move(dx, dy)

        print("Best move:", best_move)
