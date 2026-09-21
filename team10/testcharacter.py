# This is necessary to find the main code
import sys
import time
import math
sys.path.insert(0, '../bomberman')
# Import necessary stuff
from entity import CharacterEntity
from colorama import Fore, Back
import A_star
import minimax

class TestCharacter(CharacterEntity):
    def __init__(self, name, avatar, x, y):
        super().__init__(name, avatar, x, y)
        self.decision_times = []
        self.total_moves = 0
        self.previous_position = (x, y)
        
    def count_move(self):
        position = (self.x, self.y)
        if position != self.previous_position:
            self.total_moves += 1
            self.previous_position = position

    def done(self, wrld):
        self.count_move()
        print("Final total moves:", self.total_moves)

    def do(self, wrld):
        self.count_move()
        start = time.perf_counter()

        path = A_star.a_star(self,wrld,wrld.exitcell)[0]
        if(self.monster_is_close(wrld) or not path):
            dx, dy = minimax.minimax(
                        wrld, self, depth=2
                    )
        else:
            dx = path[0][0]-self.x
            dy = path[0][1]-self.y
        
        self.move(dx,dy)

        speed = time.perf_counter() - start
        self.decision_times.append(speed)

        total = sum(self.decision_times)
        mean = sum(self.decision_times) / len(self.decision_times)
        worst = max(self.decision_times)
        best = min(self.decision_times)

        print("Current decision:", round(speed, 4), "s")
        print("Total:", round(total, 4), "s")
        print("Mean:", round(mean, 4), "s")
        print("Best:", round(best, 4), "s")
        print("Worst:", round(worst, 4), "s")

        self.move(dx, dy)

    def monster_is_close(self,wrld):
        monsters = []
        for group in wrld.monsters.values():
            monsters.extend(group)
        monster_radius = 4
        for m in monsters:
            distance_to_monster = math.sqrt(math.pow(abs(self.x-m.x),2) + math.pow(abs(self.y-m.y),2))
            print(distance_to_monster)
            if(distance_to_monster < monster_radius):
                return 1
        return 0
