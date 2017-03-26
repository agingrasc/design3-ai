from enum import Enum

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

    def __init__(self):
        self.state = self.CellState.EMPTY
        self.weight = math.inf
        self.visited = False

    def update_weight(self, weight):
        if weight < self.weight:
            self.weight = weight

    def set_blocked(self):
        self.state = self.CellState.BLOCKED

    def is_blocked(self):
        return self.state == self.CellState.BLOCKED


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

    def print_grid(self):
        grid_str = ""
        for i, row in enumerate(self.rows):
            row_str = ""
            for j, col in enumerate(row):
                if i == j == 0:
                    row_str += 'O'
                elif col.is_blocked():
                    row_str += 'X'
                else:
                    row_str += ' '
            row_str += '\n'
            grid_str += row_str
        print(grid_str)

    def _init_nodes(self, x_dim, y_dim):
        for i in range(math.ceil(y_dim/self.scale)):
            col = []
            for j in range(math.ceil(x_dim/self.scale)):
                col.append(Cell())
            self.rows.append(col)

if __name__ == "__main__":
    obs = Position(400, 350), 80, ObstacleType.PASS_BY_LEFT
    grid = Grid(2200, 1000, 20, 130, [obs])
    grid.print_grid()
