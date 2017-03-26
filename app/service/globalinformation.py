import json
from typing import Tuple, List

from domain.gameboard.position import Position
from websocket import create_connection

from domain.pathfinding.dijkstra import ObstacleType

ROBOT_RADIUS = 150


class GlobalInformation:
    def __init__(self):
        self.connection = None

    def set_url(self, url: str):
        self.connection = create_connection("ws://" + url + ":3000")

    def get_robot_position(self):
        data = {}
        data["headers"] = "pull_robot_position"
        data["data"] = {}
        self.connection.send(json.dumps(data))
        robot_position_json = self.connection.recv()
        robot_position_info = json.loads(robot_position_json)
        pos_x = int(float(robot_position_info['x']))
        pos_y = int(float(robot_position_info['y']))
        theta = float(robot_position_info['theta'])
        robot_position = Position(pos_x, pos_y, theta)
        return robot_position

    def get_robot_orientation(self):
        pos = self.get_robot_position()
        return pos.theta

    def get_obstacles(self) -> List[Tuple[Position, int, ObstacleType]]:
        # pos, radius, tag
        pass

    def get_drawzone_corner_position(self):
        pass

    def get_robot_radius(self):
        return ROBOT_RADIUS

    def get_board_dimensions(self) -> Tuple[int, int]:
        # FIXME!
        return 10, 10

