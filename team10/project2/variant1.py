# This is necessary to find the main code
import sys
import time
sys.path.insert(0, '../../bomberman')
sys.path.insert(1, '..')

# Import necessary stuff
from game import Game

# TODO This is your code!
sys.path.insert(1, '../teamNN')
from learning_character import LearningCharacter

for i in range(10):
    # Create the game
    g = Game.fromfile('map.txt')

    # TODO Add your character
    g.add_character(LearningCharacter("me", # name
                                "C",  # avatar
                                0, 0  # position
    ))

    # Run!
    g.go(1)
    time.sleep(1)
