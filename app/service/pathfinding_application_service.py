from service.globalinformation import GlobalInformation
from domain.gameboard.gameboard import GameBoard
from domain.pathfinding import get_segments
from domain.pathfinding.pathfinding import PathFinding

from api.gotoposition.dimensionassembler import DimensionAssembler
from api.gotoposition.positionassembler import PositionAssembler
from api.gotoposition.obstaclesassembler import ObstacleAssembler
from domain.gameboard.bad_position_exception import BadPositionException
from domain.pathfinding.pathfinding import RobotPositionInvalid

DEFAULT_CELL_SCALE = 10
CAMERA_LENGTH = 5

dimension_assembler = DimensionAssembler(DEFAULT_CELL_SCALE)
position_assembler = PositionAssembler(DEFAULT_CELL_SCALE)
obstacle_assembler = ObstacleAssembler(position_assembler, dimension_assembler)


def find(global_information: GlobalInformation, destination):
    x_dimension, y_dimension = global_information.get_board_dimensions()
    robot_radius = global_information.get_robot_radius()
    obstacles = global_information.get_obstacles_json()

    x_dimension = int(x_dimension / DEFAULT_CELL_SCALE)
    y_dimension = int(y_dimension / DEFAULT_CELL_SCALE)
    robot_radius = int(robot_radius / DEFAULT_CELL_SCALE)
    obstacles = obstacle_assembler.convert_obstacles_from_json(obstacles)
    for obstacle in obstacles:
        print(obstacle)

    game_board = GameBoard(x_dimension, y_dimension, obstacles, robot_radius, CAMERA_LENGTH)

    robot_position_scale = __robot_position(game_board, global_information)
    destination_final = __destination_position(game_board, destination)

    pathfinder = PathFinding(game_board, robot_position_scale, destination_final)

    try:
        path = pathfinder.find_path()
    except RobotPositionInvalid:
        return find(global_information, destination)

    path = get_segments.get_filter_path(path, DEFAULT_CELL_SCALE)
    return path


def __robot_position(game_board, global_information):
    try:
        robot_position = global_information.get_robot_position()
        robot_position_scale = game_board.get_coordinate(
            int(robot_position.pos_x / DEFAULT_CELL_SCALE), int(robot_position.pos_y / DEFAULT_CELL_SCALE)
        )
        return robot_position_scale
    except BadPositionException:
        return __robot_position(game_board, global_information)


def __destination_position(game_board, destination):
    try:
        destination = game_board.get_coordinate(
            int(destination.pos_x / DEFAULT_CELL_SCALE), int(destination.pos_y / DEFAULT_CELL_SCALE)
        )
        return destination
    except BadPositionException:
        return __destination_position(game_board, destination)
