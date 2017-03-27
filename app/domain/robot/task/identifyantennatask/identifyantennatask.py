import math

import time

from domain.robot.blackboard import Blackboard
from domain.robot.task.task import Task
from domain.robot.feedback import Feedback
from service.globalinformation import GlobalInformation
from domain.command.visionregulation import VisionRegulation
from domain.command.drawer import Drawer
from domain.gameboard.position import Position
from domain.command.antenna import Antenna

LINE_LENGHT = 1
ANTENNA_DRAW_MARK_ANGLE = 0.79


class IdentifyAntennaTask(Task):
    def __init__(self,
                 drawer: Drawer,
                 antenna: Antenna,
                 feedback: Feedback,
                 vision_regulation: VisionRegulation,
                 global_information: GlobalInformation,
                 blackboard: Blackboard):
        self.drawer = drawer
        self.antenna = antenna
        self.vision_regulation = vision_regulation
        self.global_information = global_information
        self.feedback = feedback
        self.blackboard = blackboard

    def execute(self):
        start_position = self.antenna.get_start_antenna_position()
        self.vision_regulation.go_to_position(start_position)
        self.antenna.start_recording()
        end_position = self.antenna.get_stop_antenna_position()
        self.vision_regulation.go_to_position(end_position)
        self.antenna.end_recording()
        self.draw_line()
        self.feedback.send_comment("End identifying antenna")

    def draw_line(self):
        max_signal_position = self.antenna.get_max_signal_position()
        self.blackboard.antenna_position = max_signal_position
        self.vision_regulation.go_to_position(max_signal_position)

        robot_pos = self.global_information.get_robot_position()
        end_position = self.antenna.get_segment_max_signal_antenna(robot_pos)
        move_vec = Position(end_position.pos_x - robot_pos.pos_x, end_position.pos_y - robot_pos.pos_y)

        self.vision_regulation.oriente_robot(ANTENNA_DRAW_MARK_ANGLE)

        self.antenna.robot_controller.lower_pencil()
        self.antenna.robot_controller.manual_move(move_vec, Position(0, -20))
        self.antenna.robot_controller.raise_pencil()
