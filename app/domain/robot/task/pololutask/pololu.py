import time

from domain.robot.task.task import Task
from mcu.robotcontroller import RobotController


class Pololu(Task):
    def __init__(self, robot_controller: RobotController):
        self.robot_controller = robot_controller

    def execute(self):
        self.robot_controller.lower_pencil()
        time.sleep(5)
        self.robot_controller.raise_pencil()