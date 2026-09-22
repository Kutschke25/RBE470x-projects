import sys
from pathlib import Path

root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(root / "Bomberman"))

from sensed_world import SensedWorld
from events import Event
from monsters.selfpreserving_monster import SelfPreservingMonster

def hill_climbing(world, character):
    me = world.me(character)
    monsters = []

    for horde in world.monsters.values():
        for orb in horde:
            monsters.append(orb)

    detection_range = 1
    distances = get_distances(world)
    best_move = (0, 0)
    best_score = -distances.get((me.x, me.y), 10000)

    for orb in monsters:
        dis_x = abs(me.x - orb.x)
        dis_y = abs(me.y - orb.y)
        distance = max(dis_x, dis_y)

        if distance <= detection_range:
            best_score -= 0.5 * (detection_range - distance + 1)

    for dx, dy in get_moves(world, me.x, me.y):
        x, y = me.x + dx, me.y + dy

        if world.monsters_at(x, y) or world.explosion_at(x, y):
            continue

        score = -distances.get((x, y), 10000)

        for orb in monsters:
            dis_x = abs(x - orb.x)
            dis_y = abs(y - orb.y)
            distance = max(dis_x, dis_y)

            if distance <= detection_range:
                score -= 0.5 * (detection_range - distance + 1)

        if score > best_score:
            best_score = score
            best_move = (dx, dy)

    return best_move


def get_distances(world):
    distances = {world.exitcell: 0}
    queue = [world.exitcell]

    while queue:
        x, y = queue.pop(0)

        for dx, dy in get_moves(world, x, y):
            cell = (x + dx, y + dy)

            if cell not in distances:
                distances[cell] = distances[(x, y)] + 1
                queue.append(cell)

    return distances


def get_moves(world, x, y):
    moves = []

    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            nx, ny = x + dx, y + dy

            if 0 <= nx < world.width() and 0 <= ny < world.height():
                if not world.wall_at(nx, ny):
                    moves.append((dx, dy))

    return moves