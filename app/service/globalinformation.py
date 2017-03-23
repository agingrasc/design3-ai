import json
from domain.gameboard.position import Position
from websocket import create_connection


class GlobalInformation:
    def __init__(self):
        self.connection = None

    def set_url(self, url):
        self.connection = create_connection("ws://" + url + ":3000")

    def get_robot_position(self):
        data = {}
        data["headers"] = "pull_robot_position"
        data["data"] = {}
        self.connection.send(json.dumps(data))
        robot_position_json = self.connection.recv()
        robot_position_info = json.loads(robot_position_json)
        pos_x = float(robot_position_info['x'])
        pos_y = float(robot_position_info['y'])
        robot_position = Position(int(pos_x), int(pos_y))
        return robot_position

    def get_obstacles(self):
        pass

    def get_drawzone_corner_position(self):
        pass

    def get_robot_width(self):
        pass

    def get_gameboard_length(self):
        pass

    def get_gameboard_width(self):
        pass