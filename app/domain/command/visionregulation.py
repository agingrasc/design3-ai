import time
import json
from websocket import create_connection

from domain.gameboard.position import Position
from mcu.commands import regulator
from mcu import robotcontroller
from mcu.robotcontroller import RobotController

from service.globalinformation import GlobalInformation

DELTA_T = 0.1


class VisionRegulation:
    def __init__(self, robot_controller: RobotController, set_move_destination, global_information: GlobalInformation=None):
        if global_information:
            self.global_information = global_information
        self.connection = None
        self.robot_controller =robot_controller
        self.set_move_destination = set_move_destination

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
            print("####DEBUG####\n{}\n".format(position))
            self.go_to_position(position)

    def go_to_position(self, position):
        self.set_move_destination(position)
        self.robot_controller.move()

    def oriente_robot(self, theta):
        pos = self.global_information.get_robot_position()
        pos.theta = theta
        self.set_move_destination(pos)
        self.robot_controller.move()
