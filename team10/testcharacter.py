# This is necessary to find the main code
import sys
sys.path.insert(0, '../bomberman')
# Import necessary stuff
from entity import CharacterEntity
from colorama import Fore, Back
import A_star

class TestCharacter(CharacterEntity):
    def do(self, wrld):
        path = A_star.a_star(wrld)
        if(path != None):
            for node in path:   
                self.set_cell_color(node[0],node[1], Fore.RED + Back.GREEN)
        else:
            print("No Path!")

        while(1):
            if wrld.time > 4998:
                break
