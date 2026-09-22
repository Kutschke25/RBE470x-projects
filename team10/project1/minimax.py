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
    while queue:
        x, y = queue.pop(0)
        for dx, dy in get_moves(world, x, y):
            cell = (x + dx, y + dy)
            if cell not in distances:
                distances[cell] = distances[(x, y)] + 1
                queue.append(cell)

    def max_value(state, left, alpha, beta):
        for event in state.events:
            if event.tpe == Event.CHARACTER_KILLED_BY_MONSTER and event.character.name == character.name:
                return -1000000 - state.time
        for event in state.events:
            if event.tpe == Event.CHARACTER_FOUND_EXIT and event.character.name == character.name:
                return 1000000 + state.time
        player = state.me(character)
        if player is None or state.time <= 0:
            return -1000000 - state.time
        if left == 0:
            score = -420 * distances[(player.x, player.y)]
            for monster in get_monsters(state):
                distance = max(abs(player.x - monster.x), abs(player.y - monster.y))
                score -= 69 / max(1, distance)
            return score
        value = -float("inf")
        for move in get_moves(state, player.x, player.y):
            copy = SensedWorld.from_world(state)
            copy.me(character).move(*move)
            value = max(value, min_value(copy, left, alpha, beta))
            if value >= beta:
                return value
            alpha = max(alpha, value)
        return value

    def min_value(state, left, alpha, beta, first=False):
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
        value = float("inf")
        for combination in combinations:
            copy = SensedWorld.from_world(state)
            monsters = get_monsters(copy)
            for i in range(len(monsters)):
                monsters[i].move(*combination[i])
            copy, _ = copy.next()
            value = min(value, max_value(copy, left - 1, alpha, beta))
            if value <= alpha:
                return value
            beta = min(beta, value)
        return value

    best_value = -float("inf")
    best_move = (0, 0)
    for move in get_moves(world, me.x, me.y):
        copy = SensedWorld.from_world(world)
        copy.me(character).move(*move)
        value = min_value(copy, depth, best_value, float("inf"), True)
        if value > best_value:
            best_value = value
            best_move = move
    return best_move

def get_monsters(world):
    monsters = []
    for group in world.monsters.values():
        monsters.extend(group)
    return monsters

def get_moves(world, x, y):
    moves = []
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < world.width() and 0 <= ny < world.height():
                if not world.wall_at(nx, ny):
                    moves.append((dx, dy))
    return moves

def monster_moves(world, monster):
        return get_moves(world, monster.x, monster.y)
    
