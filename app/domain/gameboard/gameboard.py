import sys
import collections
from enum import Enum
from . import position

ObstacleValueObject = collections.namedtuple('ObstacleValueObject', 'pos_x pos_y radius tag')


class Tag(Enum):
    OBSTACLE = 'X'
    CAN_PASS = ' '
    ROBOT = 'R'
    CANT_PASS_RIGHT = "OCPR"
    CANT_PASS_LEFT = "OCPL"
    PATH = 'O'


class GameBoard:
    def __init__(self, width, length, obstacles, robot_radius=1):
        self.width = width
        self.length = length
        self.robot_coordinate = Coordinate(0, 0)
        self.game_board = []
        self.robot_radius = robot_radius
        self.__build_board()
        for obstacle in obstacles:
            self.__add_obstacle(obstacle)

    def set_robot_position(self, pos_x, pos_y):
        self.robot_coordinate.set_tag(Tag.CAN_PASS)
        self.robot_coordinate = self.get_coordinate(pos_x, pos_y)
        self.robot_coordinate.set_tag(Tag.ROBOT)

    def print_game_board(self):
        for i in range(0, self.width):
            line = ""
            for j in range(0, self.length):
                line += self.get_real_coordinate(i, j).get_tag().value
            print(line)

    def print_game_board_weight(self):
        for i in range(0, self.width):
            line = ""
            for j in range(0, self.length):
                if self.get_real_coordinate(i, j).weight >= (sys.maxsize):
                    line += " X "
                else:
                    line += " " + str(self.get_coordinate(i, j).weight) + " "
            print(line)

    def __add_padding_borders(self):
        for i in range(0, self.width):
            for j in range(0, self.robot_radius):
                self.get_real_coordinate(i, j).set_tag(Tag.OBSTACLE)
            for j in range(self.length - self.robot_radius, self.length):
                self.get_real_coordinate(i, j).set_tag(Tag.OBSTACLE)
        for j in range(0, self.length):
            for i in range(0, self.robot_radius):
                self.get_real_coordinate(i, j).set_tag(Tag.OBSTACLE)
            for i in range(self.width - self.robot_radius, self.width):
                self.get_real_coordinate(i, j).set_tag(Tag.OBSTACLE)

    def __build_board(self):
        for i in range(self.width - 1, -1, -1):
            row = []
            for j in range(0, self.length):
                coord = Coordinate(i, j)
                row.append(coord)
            self.game_board.append(row)
        self.__add_padding_borders()

    def __add_obstacle(self, obstacle_value_object):
        obstacles = build_obstacle(obstacle_value_object, self.width, self.length, self.robot_radius)
        for obstacle in obstacles:
            self.game_board[self.width - 1 - obstacle.pos_x][obstacle.pos_y] = obstacle

    def get_coordinate(self, x, y):
        return self.game_board[self.width - 1 - x][y]

    def get_real_coordinate(self, x, y):
        return self.game_board[x][y]


def build_obstacle(obstacle, width, length, robot_radius):
    obstacle_coord = []
    startx_pos = __verify_start_x(obstacle, robot_radius)
    starty_pos = __verify_start_y(obstacle, robot_radius)
    endx_pos = __verify_end_x(obstacle, robot_radius, width)
    endy_pos = __verify_end_y(obstacle, robot_radius, length)
    for i in range(startx_pos, endx_pos):
        for j in range(starty_pos, endy_pos):
            new_obstacle_coord = Coordinate(i, j)
            new_obstacle_coord.set_tag(Tag.OBSTACLE)
            new_obstacle_coord.set_weight(sys.maxsize)
            obstacle_coord.append(new_obstacle_coord)
    return obstacle_coord


def __verify_start_y(obstacle, robot_radius):
    starty_pos = obstacle.pos_y - obstacle.radius - robot_radius
    if starty_pos < 0 or obstacle.tag == Tag.CANT_PASS_LEFT:
        starty_pos = 0
    return starty_pos


def __verify_end_y(obstacle, robot_radius, width):
    endy_pos = obstacle.pos_y + obstacle.radius + robot_radius
    if endy_pos > width - 1 or obstacle.tag == Tag.CANT_PASS_RIGHT:
        endy_pos = width - 1
    return endy_pos


def __verify_end_x(obstacle, robot_radius, length):
    endx_pos = obstacle.pos_x + obstacle.radius + robot_radius
    if endx_pos > length - 1:
        endx_pos = length - 1
    return endx_pos


def __verify_start_x(obstacle, robot_radius):
    startx_pos = obstacle.pos_x - obstacle.radius - robot_radius
    if startx_pos < 0:
        startx_pos = 0
    return startx_pos


class Coordinate(position.Position):
    def __init__(self, pos_x, pos_y):
        position.Position.__init__(self, pos_x, pos_y)
        self.tag = Tag.CAN_PASS
        self.weight = -1

    def set_tag(self, new_tag):
        self.tag = new_tag
        if self.tag == Tag.OBSTACLE:
            self.weight = sys.maxsize

    def set_weight(self, weight):
        if self.tag == Tag.OBSTACLE:
            self.weight = sys.maxsize
        else:
            self.weight = weight

    def set_path(self):
        self.tag = Tag.PATH

    def get_tag(self):
        return self.tag
