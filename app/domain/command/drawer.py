from typing import List
from domain.gameboard.position import Position
from mcu.robotcontroller import RobotController


class Drawer:
    def __init__(self, robot_controler: RobotController):
        self.robot_controler = robot_controler

    def draw(self, segments: List[Position]):
        pass

    def stop(self):
        pass
