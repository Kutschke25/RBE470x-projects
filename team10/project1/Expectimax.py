import math
from entity import CharacterEntity
from entity import MovableEntity
from world import SensedWorld

def expectimax_search(c:CharacterEntity, world:SensedWorld):
    val = -math.inf
    a = ""
    for new_a in possibleCharacterActions():
        new_world = update_world(c, world, new_a)
        new_val = exp_value(c, new_world)
        if new_val> val:
            a = new_a
            val = new_val
    return a

def exp_value(c:CharacterEntity,world:SensedWorld):
    if(terminal_test(c,world)):
        return world.scores[c.name]
    v = 0
    for a,p in possibleMonsterActions(world):
        new_world = update_world(c, world, a)
        v += p*max_value(c,new_world)
    return v

def max_value(c:CharacterEntity,world:SensedWorld):
    if(terminal_test(c,world)):
        return world.scores[c.name]
    v = -math.inf
    for new_a in possibleCharacterActions():
        new_world = update_world(c, world, new_a)
        new_v = exp_value(c,new_world)
        if(new_v>v):
            v = new_v
    return v

def update_world(e:MovableEntity, world:SensedWorld, new_a:str):
    if(e is CharacterEntity):
        dx = 0
        dy = 0
        for a in new_a:
            match (a):
                case "b":
                    e.place_bomb()
                case "w":
                    dy = -1
                case "s":
                    dy = 1
                case "a":
                    dx = -1
                case "d":
                    dx = 1
        if(new_a != "b"):
            e.move(dx,dy)
    return world
    

def possibleCharacterActions(c:CharacterEntity, world:SensedWorld):
    possible_actions = []

    for dx in [-1,0,1]:
        if(c.x +dx >0 or c.x <world.width()):
            for dy in [-1,0,1]:
                if(c.y +dy >0 or c.y <world.height()):
                    if world.empty_at(c.x+dx, c.y+dy) or world.exit_at(c.x+dx,c.y+dy):
                        action = ""
                        if(dy == 1): action = action + "s"
                        elif(dy == -1): action = action + "w"

                        if(dx == -1): action = action + "a"
                        elif(dx == 1): action = action + "d"
                        possible_actions.append(action)

    for k,b in world.bombs.items():
        if b.owner == c:
            can_bomb = False
            break
    if can_bomb:
        possible_actions.append("b")

    return possible_actions

def possibleMonsterActions(world:SensedWorld):
    return

def terminal_test(c:CharacterEntity, world:SensedWorld):
    c_exists = True
    for k,char in world.characters:
        if(char == c):
            c_exists = False
    return c_exists