# This is necessary to find the main code
import sys
from pathlib import Path
import time
root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root / "Bomberman"))
sys.path.insert(1, str(root / "team10" / "project1"))
# Import necessary stuff
from entity import CharacterEntity
from colorama import Fore, Back
import Expectimax

class ExpectiMaxCharacter(CharacterEntity):
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

        action = Expectimax.expectimax_search(self, wrld,1)
        if(action == "b"):
            self.place_bomb()
        else:
            dx = 0
            dy = 0
            for a in action:
                match (a):
                    case "w":
                        dy = -1
                    case "s":
                        dy = 1
                    case "a":
                        dx = -1
                    case "d":
                        dx = 1
            self.move(dx,dy)

        speed = time.perf_counter() - start
        self.decision_times.append(speed)

        mean = sum(self.decision_times) / len(self.decision_times)
        worst = max(self.decision_times)

        print("Current decision:", round(speed, 4), "s")
        print("Mean:", round(mean, 4), "s")
        print("Worst:", round(worst, 4), "s")
