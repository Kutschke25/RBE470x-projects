import sys
from pathlib import Path

root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(root / "Bomberman"))

from sensed_world import SensedWorld
from events import Event
from monsters.selfpreserving_monster import SelfPreservingMonster

def minimax(world, character, depth):
    me = world.me(character)
    distances = {world.exitcell: 0}
    queue = [world.exitcell]

    #gets the distance from the exit cell to every valid cell in the grid
    while queue:
        x, y = queue.pop(0)
        for dx, dy in get_moves(world, x, y):
            cell = (x + dx, y + dy)
            if cell not in distances:
                distances[cell] = distances[(x, y)] + 1
                queue.append(cell)

    def max_value(state, left, alpha, beta):
        #terminal states based on events
        for event in state.events:
            if event.tpe == Event.CHARACTER_KILLED_BY_MONSTER and event.character.name == character.name:
                return -1000000 - state.time
        for event in state.events:
            if event.tpe == Event.CHARACTER_FOUND_EXIT and event.character.name == character.name:
                return 1000000 + state.time
        player = state.me(character)
        if player is None or state.time <= 0:
            return -1000000 - state.time
        #Exits if the depth variable was reached
        if left == 0:
            # score based on how far away from the goal
            score = -420 * distances[(player.x, player.y)]
            #score based on how far away from monsters we are
            for monster in get_monsters(state):
                distance = max(abs(player.x - monster.x), abs(player.y - monster.y))
                score -= 69 / max(1, distance)
            return score

        #Simulates every one of the possible character actions
        value = -float("inf")
        for move in get_moves(state, player.x, player.y):
            #copies the world
            copy = SensedWorld.from_world(state)
            #moves the character in the copied world
            copy.me(character).move(*move)

            #sets the value according to minimax
            value = max(value, min_value(copy, left, alpha, beta))
            #exits early accoring to beta pruning
            if value >= beta:
                return value
            #updates alpha
            alpha = max(alpha, value)
        return value

    def min_value(state, left, alpha, beta, first=False):
        #Creates an array of every possible monster movement combination
        combinations = [[]]
        for monster in get_monsters(state):
            if first:
                moves = [(monster.dx, monster.dy)]
            else:
                moves = monster_moves(state, monster)
            new_combinations = []
            for combination in combinations:
                for move in moves:
                    new_combinations.append(combination + [move])
            combinations = new_combinations

        #Simulates every one of the previously found combinations    
        value = float("inf")
        for combination in combinations:
            #copies the world
            copy = SensedWorld.from_world(state)
            #moves the monsters in accordance with the current combination
            monsters = get_monsters(copy)
            for i in range(len(monsters)):
                monsters[i].move(*combination[i])
            #moves the world state on 
            copy, _ = copy.next()

            #Sets the value according to minimax
            value = min(value, max_value(copy, left - 1, alpha, beta))
            #exits early according to alpha pruning
            if value <= alpha:
                return value
            #updates beta
            beta = min(beta, value)
        #returns the 
        return value

    #sets up a max check
    best_value = -float("inf")
    best_move = (0, 0)
    #Loops through every possible character move
    for move in get_moves(world, me.x, me.y):
        #creates a copy of the world
        copy = SensedWorld.from_world(world)
        #moves the character in the copied world
        copy.me(character).move(*move)
        #gets the min_value of that move, using alpha beta pruning
        value = min_value(copy, depth, best_value, float("inf"), True)
        #Checks to see if the move is better
        if value > best_value:
            best_value = value
            best_move = move
    #returns best_move, which has the maximum of the available values
    return best_move

def get_monsters(world):
    #returns the monsters in the world
    monsters = []
    for group in world.monsters.values():
        monsters.extend(group)
    return monsters

def get_moves(world, x, y):
    #Returns the list of valid (but not necessarily safe) moves around x,y
    moves = []
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < world.width() and 0 <= ny < world.height():
                if not world.wall_at(nx, ny):
                    moves.append((dx, dy))
    return moves

def monster_moves(world, monster):
    #Returns the list of valid (but not necessarily safe) moves around the given monster
    return get_moves(world, monster.x, monster.y)
    
