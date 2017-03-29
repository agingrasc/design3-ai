from domain.gameboard import gameboard
from domain.gameboard.gameboard import ObstacleValueObject
from domain.gameboard.position import Position
from service.globalinformation import GlobalInformation

VALID_RADIUS = 3


class DestinationCalculator():
    def __init__(self, global_information: GlobalInformation):
        self.global_information = global_information

    def get_safezone(self, obstacles, robot_position) -> Position:
        drawzone_corner_position = self.global_information.get_drawzone_corner_position(
        )
        robot_width = self.global_information.get_robot_radius()
        x_destination = drawzone_corner_position.pos_x + (
            (robot_width / 2) + 2)
        if len(obstacles) > 0:
            closer_obstacle = self.get_the_closer_obstacle(obstacles)
            if closer_obstacle.tag == gameboard.Tag.CANT_PASS_RIGHT:
                y_destination = closer_obstacle.pos_y + ((robot_width / 2) + 2)
            elif closer_obstacle.tag == gameboard.Tag.CANT_PASS_LEFT:
                y_destination = closer_obstacle.pos_y - ((robot_width / 2) + 2)
            else:
                y_destination = closer_obstacle.pos_y + ((robot_width / 2) + 2)
        else:
            y_destination = drawzone_corner_position.pos_y + (
                (robot_width / 2) + 2)

        return Position(pos_x=x_destination, pos_y=y_destination)

    def get_the_closer_obstacle(self, obstacles) -> ObstacleValueObject:
        closer_obstacle = ObstacleValueObject(
            pos_x=2300, pos_y=0, radius=VALID_RADIUS, tag="")
        for obstacle in obstacles:
            if obstacle.pos_x < closer_obstacle.pos_x:
                closer_obstacle = obstacle

        return closer_obstacle
