from typing import Tuple

from domain.gameboard.position import Position
from domain.pathfinding.dijkstra import ObstacleType
from service.globalinformation import GlobalInformation

VALID_RADIUS = 3
STOP_POSITION = Position(1250, 880, 0) # 1280, 865


class DestinationCalculator():
    def __init__(self, global_information: GlobalInformation):
        self.global_information = global_information

    def get_safezone(self, obstacles, robot_position) -> Position:
        drawzone_corner_position = self.global_information.get_drawzone_corner_position()
        robot_width = self.global_information.get_robot_radius()
        x_destination = drawzone_corner_position.pos_x + (
            (robot_width / 2) + 2)
        if len(obstacles) > 0:
            closer_obstacle = self.get_the_closer_obstacle(obstacles)
            pos, radius, obs_type = closer_obstacle
            if obs_type == ObstacleType.PASS_BY_LEFT:
                y_destination = pos.pos_y + ((robot_width / 2) + 2)
            elif obs_type == ObstacleType.PASS_BY_RIGHT:
                y_destination = pos.pos_y - ((robot_width / 2) + 2)
            else:
                y_destination = pos.pos_y + ((robot_width / 2) + 2)
        else:
            y_destination = drawzone_corner_position.pos_y + (
                (robot_width / 2) + 2)

        # return Position(x_destination, y_destination)
        return STOP_POSITION

    def get_the_closer_obstacle(self, obstacles: Tuple[Position, int, ObstacleType]):
        closer_obstacle = Position(2300, 0), VALID_RADIUS, ObstacleType.NORMAL
        for obstacle in obstacles:
            pos, radius, obs_type = obstacle
            closest_pos, closest_radius, closest_obs_type = closer_obstacle
            if pos.pos_x < closest_pos.pos_x:
                closer_obstacle = obstacle

        return closer_obstacle
