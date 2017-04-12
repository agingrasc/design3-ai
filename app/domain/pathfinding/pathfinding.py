import sys
import queue
import math
from domain.pathfinding.grid import Grid


class NoPathFound(Exception):
    pass


class RobotPositionInvalid(Exception):
    def __init__(self, position):
        message = "Robot position is invalid : " + str(position)
        Exception.__init__(self, message)


class PathFinding:
    def __init__(self, game_board, begin_position, end_position):
        self.grid = Grid(game_board)
        self.obstacles_position = game_board.obstacles_position
        self.begin_position = begin_position
        self.end_position = end_position
        self.end_position.set_weight(0)

    def find_path(self, obstacles_precision=True):
        if self.end_position.weight == sys.maxsize:
            self.end_position = find_closes_destination(self.grid, self.end_position)

        if self.begin_position.weight == sys.maxsize:
            raise RobotPositionInvalid(self.begin_position)

        initialise_weight(self.grid, self.end_position)

        path = find(
            self.grid, self.begin_position, self.end_position, self.obstacles_position, self.grid.width,
            self.grid.length, obstacles_precision
        )
        return path


def find(grid, begin_position, end_position, obstacles_position, width, length, obstacles_precision):
    path = []
    current_neighbor = begin_position
    while current_neighbor.weight > 0:
        neighbors = grid.neighbors(current_neighbor)
        new_neighbors = removed_already_visited_neighbors(neighbors, path)
        current_neighbor = find_minimum(
            new_neighbors, end_position, obstacles_position, width, length, obstacles_precision
        )
        current_neighbor.set_path()
        path.append(current_neighbor)
    return path


def find_closes_destination(grid, end_position):
    neighbors = queue.Queue()
    neighbors.put(end_position)
    current_neighbor = end_position
    visited_neighbors = []
    while current_neighbor.weight == sys.maxsize:
        current_neighbor = neighbors.get()
        new_neighbors = grid.neighbors(current_neighbor)
        for new_neighbor in new_neighbors:
            if not new_neighbor in visited_neighbors:
                visited_neighbors.append(new_neighbor)
                neighbors.put(new_neighbor)
    closest = []
    while not neighbors.empty():
        postentionnaly_closest = neighbors.get()
        if not postentionnaly_closest.weight == sys.maxsize:
            closest.append(postentionnaly_closest)
    return find_real_value_minimum(closest, end_position)


def find_real_value_minimum(neighbors, destination):
    if len(neighbors) <= 0:
        raise NoPathFound
    old_distance = sys.maxsize
    current_neighbor = neighbors[0]
    for neighbor in neighbors:
        new_distance = (neighbor.pos_x - destination.pos_x)**2 + (neighbor.pos_y - destination.pos_y)**2
        if new_distance <= old_distance:
            old_distance = new_distance
            current_neighbor = neighbor
    return current_neighbor


def distance_from_walls(neighbor, width, length):
    distance_from_y = min([neighbor.pos_y, length - neighbor.pos_y])
    return distance_from_y


def find_distance_from_closest_obstacle(neighbor, obstacles_position, width, length):
    old_distance = sys.maxsize
    for obstacle_position in obstacles_position:
        new_distance = math.sqrt(
            (neighbor.pos_x - obstacle_position.pos_x)**2 + (neighbor.pos_y - obstacle_position.pos_y)**2
        )
        if new_distance <= old_distance:
            old_distance = new_distance

    return old_distance


def find_minimum(neighbors, destination, obstacles_position, width, length, obstacles_precision):
    if len(neighbors) <= 0:
        raise NoPathFound
    current_neighbor = neighbors[0]
    new_min = []
    for neighbor in neighbors:
        if neighbor.weight < current_neighbor.weight:
            new_min = []
            current_neighbor = neighbor
            new_min.append(neighbor)
        if neighbor.weight <= current_neighbor.weight:
            new_min.append(neighbor)

    old_distance = sys.maxsize
    for neighbor in new_min:
        new_distance = math.sqrt((neighbor.pos_x - destination.pos_x)**2 + (neighbor.pos_y - destination.pos_y)**2)
        new_distance_from_obstace = find_distance_from_closest_obstacle(neighbor, obstacles_position, width, length)
        new_distance_from_walls = distance_from_walls(neighbor, width, length)
        if obstacles_precision:
            new_distance -= new_distance_from_walls
        if new_distance <= old_distance:
            old_distance = new_distance
            current_neighbor = neighbor

    return current_neighbor


def removed_already_visited_neighbors(neighbors, path):
    new_neighbors = []
    for neighbor in neighbors:
        if neighbor not in path and not (neighbor.weight == sys.maxsize):
            new_neighbors.append(neighbor)
    return new_neighbors


def initialise_weight(grid, begin_position):
    neighbors = queue.Queue()
    neighbors.put(begin_position)
    while not neighbors.empty():
        neighbor = neighbors.get()
        new_neighbors = grid.neighbors(neighbor)
        for new_neighbor in new_neighbors:
            if new_neighbor.weight == -1:
                new_neighbor.set_weight(neighbor.weight + 1)
                neighbors.put(new_neighbor)
