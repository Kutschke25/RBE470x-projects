# This is necessary to find the main code
import sys
sys.path.insert(0, '../bomberman')
# Import necessary stuff
from entity import CharacterEntity
from colorama import Fore, Back
import Expectimax

class TestCharacter(CharacterEntity):
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
