import numpy as np

from domain.command.antenna import Antenna
from domain.command.visionregulation import VisionRegulation
from domain.gameboard.position import Position
from domain.robot.blackboard import Blackboard
from domain.robot.task.task import Task
from service import pathfinding_application_service
from mcu.robotcontroller import RobotSpeed
from service.feedback import Feedback
from service.feedback import TASK_IDENTEFIE_ANTENNA
from service.globalinformation import GlobalInformation

LINE_LENGHT = 1
ANTENNA_DRAW_MARK_ANGLE = np.deg2rad(0)
ANTENNA_MARK_LENGTH = 7.5



class IdentifyAntennaTask(Task):
    def __init__(
        self,
        antenna: Antenna,
        feedback: Feedback,
        vision_regulation: VisionRegulation,
        global_information: GlobalInformation,
        blackboard: Blackboard,
        pathfinder_service: pathfinding_application_service
    ):
        self.antenna = antenna
        self.vision_regulation = vision_regulation
        self.global_information = global_information
        self.feedback = feedback
        self.blackboard = blackboard
        self.pathfinder_service = pathfinder_service

    def execute(self):
        self.antenna.robot_controller.set_robot_speed(RobotSpeed.SCAN_SPEED)
        start_position = self.antenna.get_start_antenna_position()
        path_to_start_point = self.pathfinder_service.find(self.global_information, start_position)
        self.vision_regulation.go_to_positions(path_to_start_point)
        self.antenna.start_recording()
        end_position = self.antenna.get_stop_antenna_position()
        path = self.pathfinder_service.find(self.global_information, end_position)
        self.vision_regulation.go_to_positions(path)
        self.antenna.end_recording()
        self.draw_line()
        self.vision_regulation.go_to_position(self.blackboard.antenna_position)
        self.antenna.robot_controller.set_robot_speed(RobotSpeed.NORMAL_SPEED)
        self.feedback.send_comment(TASK_IDENTEFIE_ANTENNA)

    def draw_line(self):
        max_signal_position = self.antenna.get_max_signal_position()
        self.blackboard.antenna_position = max_signal_position

        robot_pos = self.global_information.get_robot_position()
        max_position = self.antenna.get_segment_max_signal_antenna(robot_pos)
        self.global_information.send_path([robot_pos, max_position])
        move_vec = Position(0, -ANTENNA_MARK_LENGTH)
        self.vision_regulation.oriente_robot(max_signal_position.theta)
        self.vision_regulation.go_to_position(max_signal_position)
        mark_move = Position(0, -ANTENNA_MARK_LENGTH)

        self.vision_regulation.oriente_robot(ANTENNA_DRAW_MARK_ANGLE)
        self.antenna.robot_controller.lower_pencil()
        self.antenna.robot_controller.precise_move(mark_move)
        self.antenna.robot_controller.raise_pencil()
