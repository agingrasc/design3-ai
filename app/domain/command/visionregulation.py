import json
from websocket import create_connection

from mcu.robotcontroller import RobotController
from service.globalinformation import GlobalInformation

DELTA_T = 0.1


class VisionRegulation:
    def __init__(self, robot_controller: RobotController, global_information: GlobalInformation):
        self.connection = None
        self.global_information = global_information
        self.robot_controller = robot_controller

    def set_url(self, url):
        self.connection = create_connection("ws://" + url + ":3000")

    def push_path(self, path):
        new_path = []
        for pos in path:
            x = pos.pos_x
            y = pos.pos_y
            new_pos = {'x': x, 'y': y}
            new_path.append(new_pos)

        data = {}
        data["headers"] = "push_path"
        data["data"] = new_path
        self.connection.send(json.dumps(data))

    def go_to_positions(self, positions):
        for position in positions:
            print("Path position: {}".format(position))
            self.oriente_robot(position.theta)
            self.go_to_position(position)
        print("Path finisehd!")

    def go_to_position(self, position):
        self.robot_controller.move(position)
        # self.robot_controller.stupid_move(position)

    def oriente_robot(self, theta):
        pos = self.global_information.get_robot_position()
        pos.theta = theta
        self.go_to_position(pos)
