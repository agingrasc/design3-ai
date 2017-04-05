import sys
from unittest import TestCase
from domain.gameboard.gameboard import Coordinate
from domain.gameboard.gameboard import ObstacleValueObject
from domain.gameboard.gameboard import Tag
from domain.gameboard.gameboard import GameBoard
from . import pathfinding
from .grid import Grid
from domain.pathfinding import get_segments


class PathFindingITest(TestCase):
    def test_initialise_weight_one_obstacle(self):
        obstacle = ObstacleValueObject(pos_x=9, pos_y=4, radius=2, tag=Tag.CANT_PASS_LEFT)
        game_board = GameBoard(13, 13, [obstacle])

        end_position = game_board.get_coordinate(1, 1)
        begin_position = game_board.get_coordinate(10, 10)

        pathfinder = pathfinding.PathFinding(game_board, begin_position, end_position)
        pathfinder.find_path()

    def test_initialise_weight_no_obstacle(self):
        game_board = GameBoard(6, 6, [])

        end_position = game_board.get_coordinate(1, 1)
        begin_position = game_board.get_coordinate(3, 3)
        pathfinder = pathfinding.PathFinding(game_board, begin_position, end_position)

        self.validate_path(pathfinder.find_path())

    def test_find_no_obstacle(self):
        game_board = GameBoard(6, 6, [], 0)

        end_position = game_board.get_coordinate(2, 2)
        begin_position = game_board.get_coordinate(5, 5)

        pathfinder = pathfinding.PathFinding(game_board, begin_position, end_position)
        self.validate_path(pathfinder.find_path())

    def test_find_obstacle(self):
        obstacle = ObstacleValueObject(pos_x=19, pos_y=5, radius=3, tag='')
        game_board = GameBoard(55, 30, [obstacle])

        end_position = game_board.get_coordinate(50, 8)
        begin_position = game_board.get_coordinate(2, 2)

        pathfinder = pathfinding.PathFinding(game_board, begin_position, end_position)
        pathfinder.find_path()
        self.validate_path(pathfinder.find_path())

    def test_find_left_obstacle(self):
        obstacle = ObstacleValueObject(pos_x=19, pos_y=14, radius=3, tag=Tag.CANT_PASS_LEFT)
        game_board = GameBoard(55, 30, [obstacle], 3)

        end_position = game_board.get_coordinate(50, 8)
        begin_position = game_board.get_coordinate(2, 2)

        pathfinder = pathfinding.PathFinding(game_board, begin_position, end_position)
        self.validate_path(pathfinder.find_path())

    def test_find_extrem_left_right_obstacles(self):
        obstacle1 = ObstacleValueObject(pos_x=19, pos_y=20, radius=3, tag=Tag.CANT_PASS_LEFT)
        obstacle2 = ObstacleValueObject(pos_x=39, pos_y=10, radius=3, tag=Tag.CANT_PASS_RIGHT)
        game_board = GameBoard(55, 30, [obstacle1, obstacle2], 3)

        end_position = game_board.get_coordinate(50, 8)
        begin_position = game_board.get_coordinate(2, 2)

        pathfinder = pathfinding.PathFinding(game_board, begin_position, end_position)
        self.validate_path(pathfinder.find_path())

    def test_find_left_rightx2_obstacles(self):
        obstacle1 = ObstacleValueObject(pos_x=8, pos_y=20, radius=3, tag=Tag.CANT_PASS_LEFT)
        obstacle2 = ObstacleValueObject(pos_x=39, pos_y=10, radius=3, tag=Tag.CANT_PASS_RIGHT)
        obstacle3 = ObstacleValueObject(pos_x=19, pos_y=10, radius=3, tag=Tag.CANT_PASS_RIGHT)
        game_board = GameBoard(55, 30, [obstacle1, obstacle2, obstacle3], 2)

        end_position = game_board.get_coordinate(50, 8)
        begin_position = game_board.get_coordinate(2, 2)

        pathfinder = pathfinding.PathFinding(game_board, begin_position, end_position)
        self.validate_path(pathfinder.find_path())

    def test_real_value_two_obstacles(self):
        obstacle1 = ObstacleValueObject(pos_x=148, pos_y=23, radius=3, tag=Tag.CANT_PASS_LEFT)
        obstacle2 = ObstacleValueObject(pos_x=149, pos_y=80, radius=3, tag=Tag.CANT_PASS_RIGHT)
        game_board = GameBoard(230, 111, [obstacle1, obstacle2], 5, 2)

        end_position = game_board.get_coordinate(211, 104)
        begin_position = game_board.get_coordinate(56, 63)

        pathfinder = pathfinding.PathFinding(game_board, begin_position, end_position)
        self.validate_path(pathfinder.find_path())

    def test_real_value_obstacles(self):
        obstacle1 = ObstacleValueObject(pos_x=149, pos_y=70, radius=3, tag=Tag.CANT_PASS_RIGHT)
        obstacle2 = ObstacleValueObject(pos_x=149, pos_y=11, radius=3, tag=Tag.CANT_PASS_LEFT)
        game_board = GameBoard(230, 110, [obstacle1, obstacle2])

        end_position = game_board.get_coordinate(108, 80)
        begin_position = game_board.get_coordinate(217, 27)

        pathfinder = pathfinding.PathFinding(game_board, begin_position, end_position)
        self.validate_path(pathfinder.find_path())

    def test_no_obstacle_verticable(self):
        obstacle1 = ObstacleValueObject(pos_x=5, pos_y=5, radius=1, tag=Tag.CANT_PASS_RIGHT)
        game_board = GameBoard(23, 11, [obstacle1])

        end_position = game_board.get_coordinate(14, 4)
        begin_position = game_board.get_coordinate(7, 5)

        pathfinder = pathfinding.PathFinding(game_board, begin_position, end_position)
        self.validate_path(pathfinder.find_path())

    def validate_path(self, path):
        new_path = get_segments.get_filter_path(path, 10)
        for pp in new_path:
            print(pp)
        previous_weight = sys.maxsize
        for position in path:
            self.assertTrue(previous_weight > position.weight)
        self.assertTrue(path[len(path) - 1].weight == 0)
