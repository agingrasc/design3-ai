from typing import List
import numpy as np
import time

from domain.command.visionregulation import VisionRegulation
from domain.gameboard.position import Position
from mcu.commands import wrap_theta
from mcu.robotcontroller import RobotController, RobotSpeed
from service.globalinformation import GlobalInformation

DRAW_ANGLE = np.deg2rad(45)
WAIT_TIME = 2


class Drawer:
    def __init__(self, global_information: GlobalInformation, robot_controller: RobotController, vision_regulation: VisionRegulation):
        self.global_information = global_information
        self.robot_controller = robot_controller
        self.vision_regulation = vision_regulation

    def draw(self, segments: List[Position], draw_angle=DRAW_ANGLE):
        self.vision_regulation.oriente_robot(np.deg2rad(45))
        self.robot_controller.set_robot_speed(RobotSpeed.DRAW_SPEED)

        segments.append(segments.pop(0))
        self.robot_controller.lower_pencil()
        for point in segments:
            # robot_pos = self.global_information.get_robot_position()

            # vector = Position(point.pos_x - robot_pos.pos_x, point.pos_y - robot_pos.pos_y)
            # angle = vector.get_angle() + draw_angle
            # angle = wrap_theta(angle)
            # self.vision_regulation.oriente_robot(angle)

            # self.robot_controller.precise_move(vector, Position(20, 20))
            point.theta = np.deg2rad(45)
            self.vision_regulation.go_to_position(point)

        self.robot_controller.raise_pencil()

    def stop(self):
        self.robot_controller.raise_pencil()
        self.robot_controller.set_robot_speed(RobotSpeed.NORMAL_SPEED)
