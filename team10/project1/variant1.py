# This is necessary to find the main code
import sys
sys.path.insert(0, '../../Bomberman')
sys.path.insert(1, '..')

# Import necessary stuff
from game import Game

# TODO This is your code!
sys.path.insert(1, '../team10')

from testcharacter import TestCharacter
from minimaxcharacter import MiniMaxCharacter
from astar_character import A_star_character

# Create the game
g = Game.fromfile('map.txt')


# TODO Add your character
# Uncomment this if you want the test character
g.add_character(TestCharacter("me", # name
                              "C",  # avatar
                              0, 0  # position
))

# Uncomment this if you want the a star character
# g.add_character(A_star_character("me", # name
#                               "C",  # avatar
#                               0, 0  # position
# ))

# Uncomment this if you want the minimax character
# g.add_character(MiniMaxCharacter("me", # name
#                               "C",  # avatar
#                               0, 0  # position
# ))

# Run!
g.go(1)
