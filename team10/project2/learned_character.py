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
import A_star
import state_functions

class LearnedCharacter(CharacterEntity):
    def __init__(self, name, avatar, x, y):
        super().__init__(name, avatar, x, y)
        self.decision_times = []
        self.total_moves = 0
        self.previous_position = (x, y)
        #self.weights is the list of weights used in Approximate Q-Learning
        #Time spent, Distance to monster, distance to goal, distance to bomb, distance to explosions,
        #available path to goal, number of safe moves
        #initial weights before training = {-0.5,-0.5,0.5,-0.25,-0.25,0.5,0.25}
        self.weights = [-0.5,-0.5,0.5,-0.25,-0.25,0.5,0.25]
        self.learning_rate = 0.5
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
        print("Final total moves:", self.total_moves)

    def get_Q_value(self, wrld):
        Q = 0
        Q += self.weights[0] * state_functions.time_spent_function(self,wrld)
        Q += self.weights[1] * state_functions.monster_distance_function(self,wrld)
        Q += self.weights[2] * state_functions.exit_distance_function(self,wrld)
        Q += self.weights[3] * state_functions.bomb_distance_function(self,wrld)
        Q += self.weights[4] * state_functions.explosion_distance_function(self,wrld)
        Q += self.weights[5] * state_functions.is_valid_path(self,wrld)
        Q += self.weights[6] * state_functions.safe_moves_functions(self,wrld)
        return Q

    def do(self, wrld):
        #Stuff for timing/performance evaluation
        self.count_move()
        start = time.perf_counter()

        self.move(0,0)
        q_val = self.get_Q_value(wrld)

        max_value = -math.inf
        best_move = None
        #Loops through every possible character move
        for move in state_functions.get_safe_moves(self,wrld):
            #creates a copy of the world
            copy = SensedWorld.from_world(wrld)
            #moves the character in the copied world
            if(move == "b"):
                copy.me(wrld.me(self)).place_bomb()
            elif(move != None and move != "n"):
                dx =0
                dy = 0
                if(move[0] == "1"): dx = 1
                elif(move[0] == "-1"): dx = -1
                if(move[2] == "1"): dy = 1
                elif(move[2] == "-1"): dy = -1
                action = (dx,dy)
                copy.me(wrld.me(self)).move(*action)

            new_Q = self.get_Q_value(copy)
            if(new_Q > max_value):
                best_move = move
                max_value = new_Q

        regret = state_functions.give_custom_score(wrld.me(self),wrld) - (self.gamma * max_value) - q_val
        self.weights[0] += self.learning_rate * regret * state_functions.time_spent_function(self,wrld)
        self.weights[1] += self.learning_rate * regret * state_functions.monster_distance_function(self,wrld)
        self.weights[2] += self.learning_rate * regret * state_functions.exit_distance_function(self,wrld)
        self.weights[3] += self.learning_rate * regret * state_functions.bomb_distance_function(self,wrld)
        self.weights[4] += self.learning_rate * regret * state_functions.explosion_distance_function(self,wrld)
        self.weights[5] += self.learning_rate * regret * state_functions.is_valid_path(self,wrld)
        self.weights[6] += self.learning_rate * regret * state_functions.safe_moves_functions(self,wrld)

        for i in range(len(self.weights)):
            print(i," ",self.weights[i])

        if(move == "b"):
            self.place_bomb()
        elif(move != None or move != "n"):
            dx =0
            dy = 0
            if(move[0] == "1"): dx = 1
            elif(move[0] == "-1"): dx = -1
            if(move[2] == "1"): dy = 1
            elif(move[2] == "-1"): dy = -1
            self.move(dx,dy)


