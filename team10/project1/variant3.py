# This is necessary to find the main code
import sys
sys.path.insert(0, '../../bomberman')
sys.path.insert(1, '..')

# Import necessary stuff
import random
from game import Game
from monsters.selfpreserving_monster import SelfPreservingMonster

# TODO This is your code!
sys.path.insert(1, '../teamNN')
from testcharacter import TestCharacter
from minimaxcharacter import MiniMaxCharacter
from astar_character import A_star_character

# Create the game
random.seed(123) # TODO Change this if you want different random choices
g = Game.fromfile('map.txt')
g.add_monster(SelfPreservingMonster("selfpreserving", # name
                                    "S",              # avatar
                                    3, 9,             # position
                                    1                 # detection range
))

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
