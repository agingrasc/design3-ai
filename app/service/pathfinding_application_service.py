from domain.pathfinding import dijkstra
from domain.pathfinding.dijkstra import Dijkstra
from service.globalinformation import GlobalInformation


DEFAULT_CELL_SCALE = 10


def find(global_information: GlobalInformation, destination):
    robot_position = global_information.get_robot_position()
    x_dimension, y_dimension = global_information.get_board_dimensions()
    robot_radius = global_information.get_robot_radius()
    obstacles = global_information.get_obstacles()
    grid = dijkstra.Grid(x_dimension, y_dimension, DEFAULT_CELL_SCALE, robot_radius, obstacles)
    pathfinder = Dijkstra(grid)
    path = pathfinder.get_segmented_path(robot_position, destination)
    global_information.send_path(path)
    return path
