from mcu.robotcontroller import RobotController
import math


class Task():
    def __init__(self, robot_controler):
        self.robot_controller = robot_controler
        self.id_image = 3
        self.magnification = 0
        self.orientation = "north"
        self.segments_image = []

    def execute(self, x_robot_position, y_robot_position):
        pass

    def _stop(self):
        self.status_flag = 1