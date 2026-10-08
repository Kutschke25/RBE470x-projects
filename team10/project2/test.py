# This is necessary to find the main code
import sys
import random
import datetime
sys.path.insert(0, '../../bomberman')
sys.path.insert(1, '..')

# Import necessary stuff
from game import Game

# TODO This is your code!
sys.path.insert(1, '../teamNN')
from learned_character import LearnedCharacter
from monsters.selfpreserving_monster import SelfPreservingMonster

# Create the game
g = Game.fromfile('test.txt')
random.seed(datetime.datetime.now().strftime("%S")) # TODO Change this if you want different random choices
g = Game.fromfile('test.txt')
g.add_monster(SelfPreservingMonster("aggressive", # name
                                    "A",          # avatar
                                    3, 5,        # position
                                    2             # detection range
))

# TODO Add your character
g.add_character(LearnedCharacter("me", # name
                              "C",  # avatar
                              0, 0  # position
))

# Run!
g.go(1)
