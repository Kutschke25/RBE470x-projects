import math

import A_star
from events import Event

def get_function_values(me, world):
    return [
        time_spent_function(me, world),
        monster_distance_function(me, world),
        exit_distance_function(me, world),
        bomb_distance_function(me, world),
        explosion_distance_function(me, world),
        is_valid_path(me, world),
        valid_action_functions(me, world)
    ]

def get_distance_to_closest(me, things):
    #Gets the distance to the closest thing in things
    #This is useful for monsters, bombs, and explosions
    closest_distance = math.inf
    items = []

    for group in things.values():
        if isinstance(group, list):
            items.extend(group)
        else:
            items.append(group)

    for item in items:
        distance = math.sqrt((me.x - item.x)**2 + (me.y - item.y)**2)
        if distance < closest_distance:
            closest_distance = distance

    return closest_distance

def time_spent_function(me, world):
    #value function for time spent in the world
    #as the time elapses, the value increases
    #Should be paired with a negative weight, as we want a decreased time
    return 1 / (world.time + 1)

def monster_distance_function(me, world):
    #value function for distance to monsters
    #As the monster gets closer, the value increases
    #Should be paired with a negative weight, as we want to stay away from monsters
    distance = get_distance_to_closest(me, world.monsters)

    # Only react to nearby monsters.
    if distance > 3:
        return 0

    return 1 / (distance + 1)


def exit_distance_function(me, world):
    #value function for distance to exit
    #As the exit gets closer, the value increases
    #Should be paired with a positive weight, as we want to get closer to the exit
    dx = me.x - world.exitcell[0]
    dy = me.y - world.exitcell[1]
    return 1 / (math.sqrt(dx**2 + dy**2) + 1)


def bomb_distance_function(me, world):
    #value function for distance to bombs
    #As a bomb gets closer, the value increases
    #Should be paired with a negative weight, as we want to get stay away from bombs
    return 1 / (get_distance_to_closest(me, world.bombs) + 1)


def explosion_distance_function(me, world):
    #value function for distance to explosions
    #As an explosion gets closer, the value increases
    #Should be paired with a negative weight, as we want to get stay away from explosion
    return 1 / (get_distance_to_closest(me, world.explosions) + 1)


def is_valid_path(me, world):
    #Uses A_star to find a valid path to the exit
    #If it is blocked, return 0
    #If a star can find a path, return 1
    path = A_star.a_star(me, world, world.exitcell)
    return int(path is not None)


def valid_action_functions(me, world):
    # This count includes waiting and bombing, not just movement.
    return len(get_valid_actions(me, world)) / 9


def get_valid_actions(me, world):
    #waiting is always a valid action
    moves = ["n"]

    #Checks if the player can place a bomb
    can_bomb = True
    for bomb in world.bombs.values():
        if bomb.owner.name == me.name:
            can_bomb = False
            break

    if can_bomb:
        moves.append("b")

    #checks if the player can move to each of the 8 neighbor cells
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            nx, ny = me.x + dx, me.y + dy
            if 0 <= nx < world.width() and 0 <= ny < world.height():
                if world.empty_at(nx, ny) or world.exit_at(nx, ny):
                    moves.append((dx, dy))

    return moves


def give_custom_score(character, world):
    reward = -0.1

    for event in world.events:
        if event.tpe == Event.CHARACTER_KILLED_BY_MONSTER:
            if event.character.name == character.name:
                return -100

        elif event.tpe == Event.BOMB_HIT_CHARACTER:
            if event.other.name == character.name:
                return -100

        elif event.tpe == Event.CHARACTER_FOUND_EXIT:
            if event.character.name == character.name:
                return 100

        elif event.tpe == Event.BOMB_HIT_WALL:
            if event.character.name == character.name:
                reward += 1

    if world.time <= 0:
        return -100

    #reward is given for the number of walls broken
    #Otherwise, -100 is given for dying or running out of time
    #100 is given for reaching the exit
    return reward


def near_wall(me, world):
    for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        x = me.x + dx
        y = me.y + dy

        if 0 <= x < world.width() and 0 <= y < world.height():
            if world.wall_at(x, y):
                return True
    return False

#Proposed method to move a character out of a bomb's blast path
def escape_path(me, world):
    queue = [(me.x, me.y, [])]
    visited = {(me.x, me.y)}

    # Look for a cell outside the bomb's row and column
    for x, y, path in queue:
        if x != me.x and y != me.y:
            return path

        if len(path) >= world.bomb_time:
            continue

        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                nx = x + dx
                ny = y + dy

                if not (0 <= nx < world.width()
                        and 0 <= ny < world.height()):
                    continue

                if (nx, ny) in visited:
                    continue

                if not world.empty_at(nx, ny):
                    continue

                visited.add((nx, ny))
                queue.append((nx, ny, path + [(dx, dy)]))

    return None
