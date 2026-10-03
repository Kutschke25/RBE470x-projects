import math
from queue import PriorityQueue

def a_star(c,wrld,goal):
    #Sets the start position as the position of the character
    start = (c.x,c.y)

    #Creates a priority queue for ordering found cells
    frontier = PriorityQueue()
    frontier.put(start,0)
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0

    #loop to continue searching cells while there are available cells to search
    while not frontier.empty():
        current = frontier.get()

        #Break the loop if it's found the goal
        if current == goal:
            break

        #Run through every neighbor of the current cell, and assign it a priority
        for next in get_neighbors(wrld, current):
            new_cost = cost_so_far[current] + get_cost(current, next)
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + get_heuristic(next, goal)
                frontier.put(next, priority)
                came_from[next] = current

    #Return no path if all cells were exhausted and the goal wasn't found
    if(current != goal):
        return None
    else:
        #Put the path in an array by inserting each node into the beginning
        path = []
        node = current
        while node != start:
            path.insert(0,node)
            node = came_from[node]
        #return the path and the cost it took to get to the goal
        return (path,cost_so_far[current])

def get_heuristic(grid: tuple, goal: tuple):
    #heuristic is the euclidian distance between a cell and the goal, floored, and decremented by 1
    #This should make it ultra-optimistic
    return math.floor(math.sqrt(math.pow(grid[0]-goal[0],2) + math.pow(grid[1]-goal[1],2))) -1

def get_neighbors(wrld, cell: tuple):
    #Gets 8-neighbors if they are valid squares and empty or the goal
    neighbors = []
    for dx in [-1,0,1]:
        if (cell[0]+dx)>=0 and (cell[0]+dx)<wrld.width():
            for dy in [-1,0,1]:    
                if (cell[1]+dy)>=0 and (cell[1]+dy)<wrld.height():
                    if wrld.empty_at(cell[0]+dx,cell[1]+dy) or wrld.exit_at(cell[0]+dx,cell[1]+dy):  
                        neighbors.append((cell[0]+dx,cell[1]+dy))
    return neighbors

def get_cost(cell:tuple, next:tuple):
    #Used for calculating the cost between neighbors, this will either return 1 or 1.4
    return math.sqrt(math.pow(abs(cell[0]-next[0]),2) + math.pow(abs(cell[1]-next[1]),2))
