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
        #Time spent, Distance to monster, distance to goal, distance to bomb, distance to explosions, available path to goal, number of safe moves
        self.weights = [-0.5, -0.5, 0.5, -0.5, -0.25, 0.5, 0.15]
        self.learning_rate = 0.05
        self.gamma = 0.9
        self.escape_moves = None

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

        value = 0
        weights = state_functions.get_weights(me, wrld)
        for i in range(len(self.weights)):
            value += self.weights[i] * weights[i]
        return value

    def do(self, wrld):
        self.count_move()
        self.move(0, 0)

        # Follows the escape route after placing a bomb
        # if self.escape_moves is not None:
        #     if self.escape_moves:
        #         print("escaping")
        #         dx, dy = self.escape_moves.pop(0)
        #         self.move(dx, dy)
        #         return

        #     # Waits until after the explosion 
        #     # if wrld.bombs or wrld.explosions:
        #     #     # if state_functions.get_distance_to_closest(self, wrld.monsters) <= 3:
        #     #     #     break
        #     #     return

        #     self.escape_moves = None

        escape = state_functions.escape_path(self, wrld)
        q_val = self.get_Q_value(wrld)

        max_value = -math.inf
        best_move = None

        for move in state_functions.get_safe_moves(self, wrld):
            if move == "b":
                if not escape or not state_functions.near_wall(self, wrld):
                    continue

            next_world = SensedWorld.from_world(wrld)
            me = next_world.me(self)
            me.move(0, 0)

            if move == "b":
                me.place_bomb()
            elif move != "n":
                dx, dy = move
                me.move(dx, dy)

            next_world, _ = next_world.next()

            reward = state_functions.give_custom_score(self, next_world)
            if move == "b":
                reward += 1.0
            new_Q = self.get_Q_value(next_world)
            value = reward + self.gamma * new_Q

            if value > max_value:
                best_move = move
                max_value = value
            print("Move:", move, "Value:", value)

        # Updates each weight
        error = max_value - q_val
        weights = state_functions.get_weights(self, wrld)
        for i in range(len(self.weights)):
            self.weights[i] += self.learning_rate * error * weights[i]
        print("Weights:", self.weights)

        if best_move == "b":
            self.escape_moves = escape
            self.place_bomb()
        elif best_move != "n" and best_move is not None:
            dx, dy = best_move
            self.move(dx, dy)

        print("Best move:", best_move)
