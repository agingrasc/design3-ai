from typing import List
import numpy as np
import time

from domain.command.visionregulation import VisionRegulation
from domain.gameboard.position import Position
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
        self.robot_controller.set_robot_speed(RobotSpeed.DRAW_SPEED)
        robot_pos = self.global_information.get_robot_position()
        for point in segments:
            self.robot_controller.raise_pencil()
            vector = Position(robot_pos.pos_x - point.pos_x, robot_pos.pos_y - point.pos_y)
            angle = vector.get_angle() - draw_angle
            self.vision_regulation.oriente_robot(angle)
            self.robot_controller.lower_pencil()
            init_time = time.time()
            while time.time() - init_time < 1.0:
                pass
            point.theta = angle
            # FIXME!
            self.robot_controller.manual_move(point, Position(0, -20))
        self.robot_controller.raise_pencil()

    def stop(self):
        self.robot_controller.raise_pencil()
        self.robot_controller.set_robot_speed(RobotSpeed.NORMAL_SPEED)
