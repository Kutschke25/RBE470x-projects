# This is necessary to find the main code
import sys
from pathlib import Path
root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root / "Bomberman"))
sys.path.insert(1, str(root / "team10" / "project1"))
# Import necessary stuff
from entity import CharacterEntity
from colorama import Fore, Back
import Expectimax

class ExpectiMaxCharacter(CharacterEntity):
    def do(self, wrld):
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
