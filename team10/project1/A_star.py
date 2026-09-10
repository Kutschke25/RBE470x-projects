import math
from queue import PriorityQueue

def a_star(wrld):
    start = (0,0)
    goal = wrld.exitcell
    print("Goal: ",goal[0],",",goal[1])

    frontier = PriorityQueue()
    frontier.put(start,0)
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0

    while not frontier.empty():
        current = frontier.get()

        if current == goal:
            break

        for next in get_neighbors(wrld, current):
            new_cost = cost_so_far[current] + get_cost(current, next)
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + get_heuristic(next, goal)
                frontier.put(next, priority)
                came_from[next] = current

    if(current != goal):
        return None
    else:
        path = []
        node = current
        while node != start:
            path.append(node)
            node = came_from[node]
        return path

def get_heuristic(grid: tuple, goal: tuple):
    return math.floor(math.sqrt(math.pow(grid[0]+goal[0],2) + math.pow(grid[1]+goal[1],2)))

def get_neighbors(wrld, cell: tuple):
    neighbors = []
    for dx in [-1,1]:
        if (cell[0]+dx)>=0 and (cell[0]+dx)<wrld.width():
            if wrld.empty_at(cell[0]+dx,cell[1]) or wrld.exit_at(cell[0]+dx,cell[1]):  
                neighbors.append((cell[0]+dx,cell[1]))
    for dy in [-1,0,1]:    
        if (cell[1]+dy)>=0 and (cell[1]+dy)<wrld.height():
            if wrld.empty_at(cell[0],cell[1]+dy) or wrld.exit_at(cell[0],cell[1]+dy):  
                neighbors.append((cell[0],cell[1]+dy))
    return neighbors

def get_cost(cell:tuple, next:tuple):
    return 1
