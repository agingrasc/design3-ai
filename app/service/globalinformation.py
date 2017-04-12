import json

import requests
from typing import Tuple, List

from domain.gameboard.position import Position
from websocket import create_connection

from domain.pathfinding.dijkstra import ObstacleType

ROBOT_RADIUS = 100
BASE_URL_PATTERN = "http://{}:12345/{}"

DRAWZONE_CORNER_POSITION_ENDPOINT = "drawzone-corners"
TAKE_PICTURE_ENDPOINT = "take-picture"


class GlobalInformation:
    def __init__(self):
        self.connection = None
        self.base_station_url = None

    def set_url(self, url: str):
        self.base_station_url = url
        self.connection = create_connection("ws://" + url + ":3000")

    def get_robot_position(self):
        data = {'headers': 'pull_robot_position', 'data': {}}
        self.connection.send(json.dumps(data))

        try:
            robot_position_json = self.connection.recv()
        except:
            return self.get_robot_position()

        robot_position_info = json.loads(robot_position_json)
        pos_x = int(float(robot_position_info['x']))
        pos_y = int(float(robot_position_info['y']))
        theta = float(robot_position_info['theta'])
        robot_position = Position(pos_x, pos_y, theta)
        return robot_position

    def get_robot_position_json(self):
        data = {'headers': 'pull_robot_position', 'data': {}}
        self.connection.send(json.dumps(data))
        robot_position_json = self.connection.recv()
        return robot_position_json

    def get_robot_orientation(self):
        pos = self.get_robot_position()
        return pos.theta

    def get_obstacles_json(self):
        data_json = requests.get(BASE_URL_PATTERN.format(self.base_station_url, "obstacles")).json()
        obstacles = data_json['data']['obstacles']
        return obstacles

    def get_obstacles(self) -> List[Tuple[Position, int, ObstacleType]]:
        data_json = requests.get(BASE_URL_PATTERN.format(self.base_station_url, "obstacles")).json()
        obstacles = data_json['data']['obstacles']

        formated_obstacles = []
        for obstacle in obstacles:
            pos = Position(int(obstacle['position']['x']), int(obstacle['position']['y']))
            radius = int(int(obstacle['dimension']['length']) / 2)
            tag = obstacle['tag']
            if tag == "RIGHT":
                obs_type = ObstacleType.PASS_BY_RIGHT
            elif tag == "LEFT":
                obs_type = ObstacleType.PASS_BY_LEFT
            else:
                obs_type = ObstacleType.NORMAL

            obs = pos, radius, obs_type
            formated_obstacles.append(obs)

        return formated_obstacles

    def get_robot_radius(self):
        return ROBOT_RADIUS

    def get_board_dimensions(self) -> Tuple[int, int]:
        data_json = requests.get(BASE_URL_PATTERN.format(self.base_station_url, "world-dimensions")).json()
        x_dimension, y_dimension = int(float(data_json['world_dimensions']['width'])
                                       ), int(float(data_json['world_dimensions']['height']))
        return x_dimension, y_dimension

    def send_path(self, path):
        payload = {'data': {'path': []}}
        for pos in path:
            payload['data']['path'].append([pos.pos_x, pos.pos_y])

        payload_json = json.dumps(payload)
        requests.post(BASE_URL_PATTERN.format(self.base_station_url, "path"), json=payload_json)

    def send_take_picture_request(self, scale_factor, orientation):
        payload = {'data': {'scaling': scale_factor, 'orientation': orientation}}
        base_station_response = requests.post(
            BASE_URL_PATTERN.format(self.base_station_url, TAKE_PICTURE_ENDPOINT), json=payload
        ).json()
        return base_station_response

    def reset_obstacles_detection(self):
        response = requests.post(BASE_URL_PATTERN.format(self.base_station_url, "obstacles/reset")).json()
        print(response)
