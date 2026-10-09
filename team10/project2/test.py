# This is necessary to find the main code
import sys
import time
sys.path.insert(0, '../../bomberman')
sys.path.insert(1, '..')

# Import necessary stuff
import random
from game import Game
from monsters.selfpreserving_monster import SelfPreservingMonster

# TODO This is your code!
sys.path.insert(1, '../teamNN')
from learning_character import LearningCharacter
from learned_character import LearnedCharacter

new_weights =  [-5.201380847352428, 17.124917393411856, 0.18352156340527867, -1.2765390581705425]
new_character = LearningCharacter("me", # name
                                    "C",  # avatar
                                    0, 0,
                                    new_weights)

for i in range(20):
    # Create the game
    random.seed(i) # TODO Change this if you want different random choices
    # g = Game.fromfile('bomb_training.txt')

    g = Game.fromfile('test.txt')
    g.add_monster(SelfPreservingMonster("aggressive", # name
                                        "A",          # avatar
                                        3, 13,        # position
                                        2             # detection range
    ))

    # TODO Add your character
    # g.add_character(LearnedCharacter("me", # name
    #                             "C",  # avatar
    #                             0, 0  # position
    # ))

    g.add_character(new_character)

    # Run!
    g.go(1)
    new_character = LearningCharacter("me", # name
                                    "C",  # avatar
                                    0, 0,
                                    new_character.weights)
    time.sleep(5)
