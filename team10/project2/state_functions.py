import math
import A_star

#Distance to closest item
def get_distance_to_closest(me, list):
    closest_val = math.inf
    items = []
    for group in list.values():
        items.extend(group)
    if(len(items)>0):
        for i in range(1,len(items)):
            new_val = math.sqrt(math.pow((me.x-items[i].x),2) + math.pow((me.y-items[i].y),2))
            if(new_val < closet_val):
                closet_val = new_val
    return closest_val

#function for time spent in game
def time_spent_function(me,world):
    return 1 / (world.time + 1)

#function for distance to closest monster
def monster_distance_function(me, world):
    return 1 / (get_distance_to_closest(me, world.monsters) +1)

#Distance to Goal
def exit_distance_function(me, world):
    return 1 / (math.sqrt(math.pow((me.x-world.exitcell[0]),2) + math.pow((me.y-world.exitcell[1]),2)) +1)

#Distance to Bomb
def bomb_distance_function(me, world):
    return 1 / (get_distance_to_closest(me, world.bombs) +1)

#Distance to Explosion
def explosion_distance_function(me, world):
    return 1 / (get_distance_to_closest(me, world.explosions)+1)

#Valid Path To Goal
def is_valid_path(me,world):
    path = A_star.a_star(me,world,world.exitcell)
    if(path):
        return 1
    else:
        return 0

#Number of Safe Moves
#A character has 9 max moves when it is not trapped by hazards and can place a bomb.
#The more moves available to the character, the better chance it has of surviving
def safe_moves_functions(me,world):
    return len(get_safe_moves(me,world)) / 9

def get_safe_moves(me, world):
    moves = []
    moves.append("n")
    for b in world.bombs.values():
        if(b.owner == world.me(me)):
            moves.append("b")

    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            nx, ny = me.x + dx, me.y + dy
            if 0 <= nx < world.width() and 0 <= ny < world.height():
                if world.empty_at(nx,ny) or world.exit_at(nx,ny):
                    moves.append(("",dx,dy))

    return moves

def give_custom_score(character, world):
    for event in world.events:
        if event.tpe == Event.CHARACTER_KILLED_BY_MONSTER and event.character.name == character.name:
            return -1000000 - world.time
        if event.tpe == Event.BOMB_HIT_CHARACTER and event.character.name == character.name:
            return -1000000 - world.time
        if event.tpe == Event.CHARACTER_FOUND_EXIT and event.character.name == character.name:
            return 1000000 - world.time
    return 1