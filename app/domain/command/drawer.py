from typing import List
import numpy as np
import time

from domain.command.visionregulation import VisionRegulation
from domain.gameboard.position import Position
from mcu.robotcontroller import RobotController

DRAW_ANGLE = np.deg2rad(45)
WAIT_TIME = 2


class Drawer:
    def __init__(self, robot_controller: RobotController, vision_regulation: VisionRegulation):
        self.robot_controller = robot_controller
        self.vision_regulation = vision_regulation

    def draw(self, segments: List[Position]):
        self.robot_controller.lower_pencil()
        time.sleep(WAIT_TIME)
        for point in segments:
            angle = point.get_angle() + DRAW_ANGLE
            self.vision_regulation.oriente_robot(angle)
            point.theta = angle
            self.vision_regulation.go_to_position(point)

    def stop(self):
        self.robot_controller.raise_pencil()
