import math
from events import Event
from entity import CharacterEntity,MovableEntity, MonsterEntity
from sensed_world import SensedWorld
import A_star

def expectimax_search(c:CharacterEntity, world:SensedWorld, depth:int):
    val = -math.inf
    a = ""
    #Choosing the max value from possible character actions
    for new_a in possibleCharacterActions(c,world):
        #print("New a: ",c.x,c.y,new_a)
        #The value is evaluated from the expected value of the monsters 
        new_val = exp_value(c, character_action(c, world, new_a), depth)
        #print(new_a,new_val)
        if new_val> val:
            a = new_a
            val = new_val
    #print("Final: ",a,val)
    return a

def exp_value(c:CharacterEntity,new_state:tuple[SensedWorld,list], depth:int):
 #   print("EXP VALUE____________")
    (new_world,happenings) = new_state
    for e in happenings:  
        match(e.tpe):
            case Event.CHARACTER_FOUND_EXIT:
                #print("E Terminal! Found Exit")
                return 10000 + new_world.time
            case Event.CHARACTER_KILLED_BY_MONSTER:
                #print("E Terminal! Killed")
                return -10000
            case Event.BOMB_HIT_CHARACTER:
                #print("E Terminal! Blew up")
                return -10000
    if(depth<=0):
        c_val = character_value(new_world.me(c),new_world)
        #print("E Terminal!", new_world.me(c).x,new_world.me(c).y, new_world.scores[c.name],c_val)
        return c_val
    else:
        depth-=1
    v = 0
    for k,m in new_world.monsters.items():
        for a,p in possibleMonsterActions(m[0], new_world).items():
            v += p*max_value(new_world.me(c),new_world.next(),depth)
    #print("E",v)
    return v

def max_value(c:CharacterEntity,new_state:tuple[SensedWorld,list],depth:int):
  #  print("MAX VALUE____________")
    (new_world,happenings) = new_state
    for e in happenings:
        match(e.tpe):
            case Event.CHARACTER_FOUND_EXIT:
                #print("M Terminal! Found Exit")
                return 10000 + new_world.time
            case Event.CHARACTER_KILLED_BY_MONSTER:
                #print("M Terminal! Killed")
                return -10000
            case Event.BOMB_HIT_CHARACTER:
                #print("M Terminal! Blew up")
                return -10000
    if(depth<=0):
        c_val = character_value(new_world.me(c),new_world)
        #print("M Terminal!", new_world.me(c).x,new_world.me(c).y, new_world.scores[c.name],c_val)
        return c_val
    else:
        depth-=1
    v = -math.inf
    for new_a in possibleCharacterActions(new_world.me(c),new_world):
        new_v = exp_value(new_world.me(c),character_action(new_world.me(c), new_world, new_a),depth)
        #print("M", new_a,new_v)
        if(new_v>v):
            v = new_v
    return v

def character_action(c:CharacterEntity, world:SensedWorld, new_a:str):
    dx = 0
    dy = 0
    if(new_a == "b"):
        world.me(c).place_bomb()
    else:
        for a in new_a:
            match (a):
                case "w":
                    dy = -1
                case "s":
                    dy = 1
                case "a":
                    dx = -1
                case "d":
                    dx = 1
 #   print("~",dx,dy)
    world.me(c).move(dx,dy)
 #   print("!",world.me(c).dx,world.me(c).dy)
  #  print("@",world.me(c).x,world.me(c).y)
    (new_world,new_events) = world.next()
    if(new_world.me(c)):
      new_world.me(c).move(0,0)
   #   print("#",new_world.me(c).dx,new_world.me(c).dy)
    #  print("$",new_world.me(c).x,new_world.me(c).y)
    return (new_world,new_events)
    

def possibleCharacterActions(c:CharacterEntity, world:SensedWorld):
    possible_actions = []

    for dx in [-1,0,1]:
        if(c.x +dx >=0 and c.x+dx <world.width()):
            for dy in [-1,0,1]:
                if(c.y +dy >=0 and c.y+dy <world.height()):
                    if world.empty_at(c.x+dx, c.y+dy) or world.exit_at(c.x+dx,c.y+dy):
                        action = ""
                        if(dy == 1): action = action + "s"
                        elif(dy == -1): action = action + "w"

                        if(dx == -1): action = action + "a"
                        elif(dx == 1): action = action + "d"
                        possible_actions.append(action)

    can_bomb = True
    for k,b in world.bombs.items():
        if b.owner == c:
            can_bomb = False
            break
    if can_bomb:
        possible_actions.append("b")

    #print(possible_actions)
    return possible_actions

def possibleMonsterActions(m: MonsterEntity, world:SensedWorld):
    pre_possibleMonsterActions = []
    for dx in [-1,0,1]:
        if(m.x +dx >0 and m.x+dx <world.width()):
            for dy in [-1,0,1]:
                if(m.y +dy >0 and m.y+dy <world.height()):
                    if world.empty_at(m.x+dx, m.y+dy) or world.exit_at(m.x+dx,m.y+dy):
                        action = ""
                        if(dy == 1): action = action + "s"
                        elif(dy == -1): action = action + "w"

                        if(dx == -1): action = action + "a"
                        elif(dx == 1): action = action + "d"
                        pre_possibleMonsterActions.append(action)

    possibleMonsterActions = {}
    for a in pre_possibleMonsterActions:
        possibleMonsterActions[a] = 1.0 / len(pre_possibleMonsterActions)
    return possibleMonsterActions

def character_value(c:CharacterEntity,world:SensedWorld):
    time_weight = 0.1
    distance = math.floor((math.sqrt(math.pow(world.exitcell[0]-world.me(c).x,2) + math.pow(world.exitcell[1]-world.me(c).y,2))))-1
    path_goal = A_star.a_star(c,world,world.exitcell)
    if(path_goal):
       # print("Cost goal:",path_goal[1])
       # print("distance goal:",distance)
        return time_weight*world.time + (1-time_weight)/(distance+path_goal[1])
    else:
        return time_weight*world.time + (1-time_weight)/(distance)