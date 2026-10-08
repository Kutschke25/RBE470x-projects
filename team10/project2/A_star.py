import math
from queue import PriorityQueue


def a_star(character, world, goal):
    #Sets the start position as the position of the character
    start = (character.x, character.y)

    #Creates a priority queue for ordering found cells
    frontier = PriorityQueue()
    frontier.put((0, start))
    came_from = {start: None}
    cost_so_far = {start: 0}

    #loop to continue searching cells while there are available cells to search
    while not frontier.empty():
        _, current = frontier.get()

        #Break the loop if it's found the goal
        if current == goal:
            break

        #Run through every neighbor of the current cell, and assign it a priority
        for neighbor in get_neighbors(world, current):
            new_cost = cost_so_far[current] + get_cost(current, neighbor)
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                priority = new_cost + get_heuristic(neighbor, goal)
                frontier.put((priority, neighbor))
                came_from[neighbor] = current

    #Return no path if all cells were exhausted and the goal wasn't found
    if current != goal:
        return None

    # Trace the path backward from the goal, leaving out the start cell.
    path = []
    node = current
    while node != start:
        path.insert(0, node)
        node = came_from[node]
    return path, cost_so_far[current]


def get_heuristic(cell, goal):
    # Round down and subtract one to keep the estimate optimistic.
    return math.floor(get_cost(cell, goal)) - 1


def get_neighbors(world, cell):
    #Gets 8-neighbors if they are valid squares and empty or the goal
    neighbors = []
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            x = cell[0] + dx
            y = cell[1] + dy
            if 0 <= x < world.width() and 0 <= y < world.height():
                if world.empty_at(x, y) or world.exit_at(x, y):
                    neighbors.append((x, y))
    return neighbors


def get_cost(cell, neighbor):
    # Straight steps cost 1; diagonal steps cost sqrt(2).
    dx = cell[0] - neighbor[0]
    dy = cell[1] - neighbor[1]
    # if dx == 0 and dy == 0:
    #     return 0
    # else:
    #     return 1
    return math.sqrt(dx**2 + dy**2)
