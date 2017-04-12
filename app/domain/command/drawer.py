from typing import List
import numpy as np
import time

from domain.command.visionregulation import VisionRegulation
from domain.gameboard.position import Position
from domain.robot.blackboard import Blackboard
from mcu.regulator import wrap_theta
from mcu.robotcontroller import RobotController, RobotSpeed
from service.globalinformation import GlobalInformation

DRAW_ANGLE = np.deg2rad(45)
WAIT_TIME = 3


class Drawer:
    def __init__(
        self,
        global_information: GlobalInformation,
        robot_controller: RobotController,
        vision_regulation: VisionRegulation,
        blackboard: Blackboard
    ):
        self.global_information = global_information
        self.robot_controller = robot_controller
        self.vision_regulation = vision_regulation
        self.blackboard = blackboard

    def draw(self, segments: List[Position], draw_angle=DRAW_ANGLE):
        self.robot_controller.set_robot_speed(RobotSpeed.DRAW_SPEED)

        self.vision_regulation.go_to_position(segments[0])
        time.sleep(WAIT_TIME)
        self.robot_controller.lower_pencil()
        for destination in segments[1:]:
            angle = self.compute_draw_angle(destination, draw_angle)
            self.vision_regulation.oriente_robot(angle)
            destination.theta = angle
            self.vision_regulation.go_to_position(destination)

        self.stop()

    def compute_draw_angle(self, destination: Position, draw_angle) -> float:
        robot_position = self.global_information.get_robot_position()
        robot_angle = robot_position.theta
        direction_vector = destination - robot_position
        angle = direction_vector.get_angle() - draw_angle
        nearest_angle = _get_nearest_angle(angle, robot_angle)
        return wrap_theta(nearest_angle)

    def stop(self):
        self.robot_controller.raise_pencil()
        self.robot_controller.set_robot_speed(RobotSpeed.NORMAL_SPEED)


def _get_nearest_angle(angle, robot_angle):
    valid_angles = [wrap_theta((angle + np.deg2rad(90 * i))) for i in range(4)]
    shortest_delta = np.pi
    shortest_idx = 0

    for idx, angle in enumerate(valid_angles):
        delta_angle = abs(wrap_theta(angle - robot_angle))
        if delta_angle < shortest_delta:
            shortest_delta = delta_angle
            shortest_idx = idx
    return valid_angles[shortest_idx]

