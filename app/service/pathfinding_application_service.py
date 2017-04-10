from service.globalinformation import GlobalInformation
from domain.gameboard.gameboard import GameBoard
from domain.pathfinding import get_segments
from domain.pathfinding.pathfinding import PathFinding

from api.gotoposition.dimensionassembler import DimensionAssembler
from api.gotoposition.positionassembler import PositionAssembler
from api.gotoposition.obstaclesassembler import ObstacleAssembler

DEFAULT_CELL_SCALE = 10
CAMERA_LENGTH = 5

dimension_assembler = DimensionAssembler(DEFAULT_CELL_SCALE)
position_assembler = PositionAssembler(DEFAULT_CELL_SCALE)
obstacle_assembler = ObstacleAssembler(position_assembler, dimension_assembler)


def find(global_information: GlobalInformation, destination):
    robot_position = global_information.get_robot_position()
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
    robot_position_scale = game_board.get_coordinate(
        int(robot_position.pos_x / DEFAULT_CELL_SCALE), int(robot_position.pos_y / DEFAULT_CELL_SCALE)
    )
    destination = game_board.get_coordinate(
        int(destination.pos_x / DEFAULT_CELL_SCALE), int(destination.pos_y / DEFAULT_CELL_SCALE)
    )

    pathfinder = PathFinding(game_board, robot_position_scale, destination)
    path = get_segments.get_filter_path(pathfinder.find_path(), DEFAULT_CELL_SCALE)
    for pos in path:
        print(pos)
    return path
