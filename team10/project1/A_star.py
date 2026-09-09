import math
from queue import PriorityQueue

def a_star(width: int, height: int, start: tuple, goal : tuple):
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

        for next in get_neighbors(width, height, current):
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
        node = came_from.pop()
        while node != start:
            path.append(node)
            node = came_from[node]
        return path

def get_heuristic(grid: tuple, goal: tuple):
    return math.sqrt(grid[0]*goal[0] + grid[1]+goal[1])

def get_neighbors(width: int, height: int, cell: tuple):
    neighbors = []
    if cell[0] > 0:
        neighbors.append((cell[0]-1,cell[0]))
        if cell[1] > 0:
            neighbors.append((cell[0]-1,cell[0]-1))
        if cell[1] < height-1:
            neighbors.append((cell[0]-1,cell[0]+1))
    elif cell[0] < width-1:
        neighbors.append((cell[0]+1,cell[0]))
        if cell[1] > 0:
            neighbors.append((cell[0]+1,cell[0]-1))
        if cell[1] < height-1:
            neighbors.append((cell[0]+1,cell[0]+1))
    else:
        if cell[1] > 0:
            neighbors.append((cell[0],cell[0]-1))
        if cell[1] < height-1:
            neighbors.append((cell[0],cell[0]+1))
    return neighbors

def get_cost(cell:tuple, next:tuple):
    return 1
