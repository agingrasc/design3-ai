from mcu.robotcontroller import RobotController
import math


class task():
    def __init__(self, robot_controler = None):
        if robot_controler:
            self.robot_controller = robot_controler
        else:
            self.robot_controller = RobotController()
        self.id_image = 3
        self.magnification = 0
        self.orientation = "north"
        self.segments_image = []

    def execute(self, x_robot_position, y_robot_position):
        pass

    def _distance(self, x_point1, y_point1, x_point2, y_point2):
        return math.sqrt((x_point1 - x_point2) ** 2 + (y_point1 - y_point2) ** 2)