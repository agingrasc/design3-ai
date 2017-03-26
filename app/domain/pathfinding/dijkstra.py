from enum import Enum
import heapq

import math
from typing import List, Tuple

from domain.gameboard.position import Position


PADDING = 20


class ObstacleType(Enum):
    NORMAL = 0
    PASS_BY_LEFT = 1
    PASS_BY_RIGHT = 2


class Cell:

    class CellState(Enum):
        EMPTY = 0
        BLOCKED = 1
        PATH = 2

    def __init__(self, j, i):
        self.state = self.CellState.EMPTY
        self.weight = math.inf
        self.visited = False
        self.i = i
        self.j = j
        self.previous = None

    def update_weight(self, weight):
        if weight < self.weight:
            self.weight = weight

    def set_blocked(self):
        self.state = self.CellState.BLOCKED

    def is_blocked(self):
        return self.state == self.CellState.BLOCKED

    def is_path(self):
        return self.state == self.CellState.PATH

    def get_coordinate(self):
        return self.i, self.j

    def mark_path(self):
        self.state = self.CellState.PATH

    def __eq__(self, other):
        return other.weight == self.weight

    def __lt__(self, other):
        return self.weight < other.weight and not self.weight == other.weight


class Grid:
    def __init__(self, x_dim: int, y_dim: int, scale: int, robot_radius: int, obstacles: List[Tuple[Position, int, ]]):
        self.scale = scale
        self.x_dim = x_dim
        self.y_dim = y_dim
        self.i_dim = math.ceil(x_dim/self.scale)
        self.j_dim = math.ceil(y_dim/self.scale)
        self.rows: List[List[Cell]] = []
        self.robot_radius = robot_radius

        self._init_nodes(x_dim, y_dim)
        self.block_wall()
        for obstacle in obstacles:
            self.place_obstacle(obstacle)

    def block_wall(self):
        # mur en X
        j_min = 0
        j_max = self.j_dim - 1
        for i in range(self.i_dim):
            self.get_element(i, j_min).set_blocked()
            self.get_element(i, j_max).set_blocked()
        # mur en Y
        i_min = 0
        i_max = self.i_dim - 1
        for j in range(self.j_dim):
            self.get_element(i_min, j).set_blocked()
            self.get_element(i_max, j).set_blocked()

    def place_obstacle(self, obstacle: Tuple[Position, int, ObstacleType]):
        pos, radius, obs_type = obstacle
        effective_radius = radius + self.robot_radius + PADDING
        min_x, min_y = pos.pos_x - effective_radius, pos.pos_y - effective_radius
        min_x, min_y = self.set_inbound(min_x, min_y)
        max_x, max_y = pos.pos_x + effective_radius, pos.pos_y + effective_radius
        max_x, max_y = self.set_inbound(max_x, max_y)

        if obs_type == ObstacleType.PASS_BY_LEFT:
            max_y = self.y_dim - self.scale
        elif obs_type == ObstacleType.PASS_BY_RIGHT:
            min_y = 0

        for i in range(min_x, max_x, self.scale):
            for j in range(min_y, max_y, self.scale):
                self.get_cell(i, j).set_blocked()

    def set_inbound(self, x, y) -> Tuple[int, int]:
        real_x = x
        real_y = y
        if x < 0:
            real_x = 0
        elif x > self.x_dim:
            real_x = self.x_dim - self.scale

        if y < 0:
            real_y = 0
        elif y > self.y_dim:
            real_y = self.y_dim - self.scale

        return real_x, real_y

    def get_cell(self, x, y) -> Cell:
        i = math.ceil(x/self.scale)
        j = math.ceil(y/self.scale)
        return self.get_element(i, j)

    def get_element(self, i, j):
        return self.rows[j][i]

    def get_weigth(self, x, y):
        return self.get_cell(x, y).weight

    def update_weight(self, x, y, weigth):
        self.get_cell(x, y).update_weight(weigth)

    def visit(self, x, y):
        self.get_cell(x, y).visited = True

    def is_visited(self, x, y):
        return self.get_cell(x, y).visited

    def get_neighbors(self, cell: Cell) -> List[Cell]:
        i, j = cell.get_coordinate()
        neighbor = []
        if i - 1 >= 0:
            neighbor.append(self.get_element(i-1, j))
        if i + 1 < self.i_dim:
            neighbor.append(self.get_element(i+1, j))
        if j - 1 >= 0:
            neighbor.append(self.get_element(i, j-1))
        if j + 1 < self.j_dim:
            neighbor.append(self.get_element(i, j+1))
        return neighbor

    def print_grid(self):
        grid_str = ""
        for i, row in enumerate(self.rows):
            row_str = ""
            for j, col in enumerate(row):
                if i == j == 0:
                    row_str += 'O'
                elif col.is_blocked():
                    row_str += 'X'
                elif col.is_path():
                    row_str += '+'
                else:
                    row_str += ' '
            row_str += '\n'
            grid_str += row_str
        print(grid_str)

    def _init_nodes(self, x_dim, y_dim):
        for j in range(math.ceil(y_dim/self.scale)):
            col = []
            for i in range(math.ceil(x_dim/self.scale)):
                col.append(Cell(j, i))
            self.rows.append(col)

    def iter(self):
        for j in range(self.j_dim):
            for i in range(self.i_dim):
                yield self.rows[j][i]


"""https://joernhees.de/blog/2010/07/19/min-heap-in-python/"""
class Heap:
    """ A neat min-heap wrapper which allows storing items by priority
        and get the lowest item out first (pop()).
        Also implements the iterator-methods, so can be used in a for
        loop, which will loop through all items in increasing priority order.
        Remember that accessing the items like this will iteratively call
        pop(), and hence empties the heap! """

    def __init__(self):
        """ create a new min-heap. """
        self._heap = []

    def push(self, priority, item):
        """ Push an item with priority into the heap.
            Priority 0 is the highest, which means that such an item will
            be popped first."""
        assert priority >= 0
        heapq.heappush(self._heap, (priority, item))

    def pop(self):
        """ Returns the item with lowest priority. """
        item = heapq.heappop(self._heap)[1] # (prio, item)[1] == item
        return item

    def __len__(self):
        return len(self._heap)

    def __next__(self):
        return self.next()

    def next(self):
        """ Get all elements ordered by their priority (lowest first). """
        try:
            return self.pop()
        except IndexError:
            raise StopIteration


class Dijkstra:
    def __init__(self, grid: Grid):
        self.heap = Heap()
        self.grid = grid

    def get_path(self, robot_position: Position, target_position: Position) -> List[Position]:
        x, y = robot_position.pos_x , robot_position.pos_y
        init_cell = self.grid.get_cell(x, y)
        init_cell.update_weight(0)
        init_cell.mark_path()
        self.heap.push(init_cell.weight, init_cell)

        try:
            while True:
                work_cell = self.heap.pop()
                if work_cell.visited:
                    continue
                for neighbor in self.grid.get_neighbors(work_cell):
                    if not neighbor.visited and not neighbor.is_blocked():
                        neighbor.update_weight(work_cell.weight+1)
                        neighbor.previous = work_cell
                        self.heap.push(neighbor.weight, neighbor)
                work_cell.visited = True
        except IndexError:
            pass

        target_x, target_y = target_position.pos_x, target_position.pos_y
        target_cell = self.grid.get_cell(target_x, target_y)
        target_cell.mark_path()
        path = [target_cell]
        prev_cell: Cell = target_cell.previous

        while prev_cell is not init_cell:
            prev_cell.mark_path()
            path.append(prev_cell)
            prev_cell = prev_cell.previous
        path.append(init_cell)
        path.reverse()

        return [Position(int(point.i * self.grid.scale + self.grid.scale/2), int(point.j * self.grid.scale + self.grid.scale/2), robot_position.theta) for point in path]


if __name__ == "__main__":
    obs1 = Position(400, 350), 80, ObstacleType.NORMAL
    obs2 = Position(600, 600), 80, ObstacleType.PASS_BY_RIGHT
    test_grid = Grid(2200, 1000, 20, 130, [obs1, obs2])
    dijkstra = Dijkstra(test_grid)
    path = dijkstra.get_path(Position(100, 100), Position(2100, 100))
    for idx, pos in enumerate(path):
        print("Pos ({}): {} -- {} -- {}\n".format(idx, pos.pos_x, pos.pos_y, pos.theta))
    test_grid.print_grid()
