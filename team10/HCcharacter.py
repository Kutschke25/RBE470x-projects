import sys
import time
from pathlib import Path

root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root / "Bomberman"))
sys.path.insert(1, str(root / "team10" / "project1"))

from entity import CharacterEntity
import localsearch


class HCharacter(CharacterEntity):
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

    def do(self, wrld):
        self.count_move()

        start = time.perf_counter()
        dx, dy = localsearch.hill_climbing(wrld, self)
        elapsed = time.perf_counter() - start

        self.decision_times.append(elapsed)
        average = sum(self.decision_times) / len(self.decision_times)

        print("Current decision:", round(elapsed, 6), "s")
        print("Mean:", round(average, 6), "s")
        print("Worst:", round(max(self.decision_times), 6), "s")
        print("Total moves:", self.total_moves)

        self.move(dx, dy)

    def done(self, wrld):
        self.count_move()
        print("Final total moves:", self.total_moves)