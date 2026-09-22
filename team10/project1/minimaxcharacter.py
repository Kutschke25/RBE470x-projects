import sys
from pathlib import Path
import time

root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root / "Bomberman"))
sys.path.insert(1, str(root / "team10" / "project1"))

from entity import CharacterEntity
import minimax


class MiniMaxCharacter(CharacterEntity):

    def __init__(self, name, avatar, x, y):
        super().__init__(name, avatar, x, y)
        self.decision_times = []
        self.total_moves = 0
        self.previous_position = (x, y)
        
    def count_move(self):
        #if the character changed position, increment the total move counter
        position = (self.x, self.y)
        if position != self.previous_position:
            self.total_moves += 1
            self.previous_position = position

    def done(self, wrld):
        #adds up the total moves the character made
        self.count_move()
        print("Final total moves:", self.total_moves)
        

    def do(self, wrld):
        #Stuff for timing/performance evaluation
        self.count_move()
        me = wrld.me(self)

        if me is None:
            self.move(0, 0)
            return

        start = time.perf_counter()

        #_____________________________________________________________________________
        #Find a path to the goal using minimax with a depth of 2
        dx, dy = minimax.minimax(
            wrld, self, depth=2
        )
        
        self.move(dx, dy)

        #_____________________________________________________________________________

        
        #Stuff for timing/performance evaluation
        speed = time.perf_counter() - start
        self.decision_times.append(speed)

        total = sum(self.decision_times)
        mean = sum(self.decision_times) / len(self.decision_times)
        worst = max(self.decision_times)

        print("Current decision:", round(speed, 4), "s")
        print("Total:", round(total, 4), "s")
        print("Mean:", round(mean, 4), "s")
        print("Worst:", round(worst, 4), "s")
