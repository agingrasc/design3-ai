from typing import List
import numpy as np
import time

from domain.command.visionregulation import VisionRegulation
from domain.gameboard.position import Position
from mcu.regulator import wrap_theta
from mcu.robotcontroller import RobotController, RobotSpeed
from service.globalinformation import GlobalInformation

DRAW_ANGLE = np.deg2rad(-90)
WAIT_TIME = 2


class Drawer:
    def __init__(
        self,
        global_information: GlobalInformation,
        robot_controller: RobotController,
        vision_regulation: VisionRegulation
    ):
        self.global_information = global_information
        self.robot_controller = robot_controller
        self.vision_regulation = vision_regulation

    def draw(self, segments: List[Position], draw_angle=DRAW_ANGLE):
        self.robot_controller.set_robot_speed(RobotSpeed.DRAW_SPEED)

        # segments.append(segments.pop(0))
        self.robot_controller.lower_pencil()
        robot_position = self.global_information.get_robot_position()
        last_point = robot_position
        for point in segments:
            # self.vision_regulation.go_to_position(last_point)
            robot_position = self.global_information.get_robot_position()
            angle = self.compute_draw_angle(point)
            self.vision_regulation.oriente_robot(angle)
            point.theta = angle
            self.vision_regulation.go_to_position(point)
            # self.vision_regulation.robot_controller.stupid_move(point, 80, robot_position)
            # last_point = point

        self.stop()

    def compute_draw_angle(self, destination: Position) -> float:
        robot_position = self.global_information.get_robot_position()
        delta_vec = Position(destination.pos_x - robot_position.pos_x, destination.pos_y - robot_position.pos_y)
        angle = delta_vec.get_angle() + DRAW_ANGLE
        return wrap_theta(angle)


    def stop(self):
        self.robot_controller.raise_pencil()
        self.robot_controller.set_robot_speed(RobotSpeed.NORMAL_SPEED)
