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

ANTENNA_DRAW_MARK_ANGLE = np.deg2rad(0)



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
        robot_position = self.global_information.get_robot_position()
        self.antenna.robot_controller.set_robot_speed(RobotSpeed.SCAN_SPEED)
        start_position = self.antenna.get_start_antenna_position()
        path_to_start_point = self.pathfinder_service.find(self.global_information, start_position)
        self.global_information.send_path([robot_position] + path_to_start_point)
        self.vision_regulation.go_to_positions(path_to_start_point)
        self.antenna.start_recording()
        end_position = self.antenna.get_stop_antenna_position()
        path_end_position = self.pathfinder_service.find(self.global_information, end_position)
        robot_position = self.global_information.get_robot_position()
        self.global_information.send_path([robot_position] + path_end_position)
        self.vision_regulation.go_to_positions(path_end_position)
        self.antenna.end_recording()
        self.draw_line()
        self.vision_regulation.go_to_position(self.blackboard.antenna_position)
        self.antenna.robot_controller.set_robot_speed(RobotSpeed.NORMAL_SPEED)
        self.feedback.send_comment(TASK_IDENTEFIE_ANTENNA)

    def draw_line(self):
        robot_position = self.global_information.get_robot_position()
        self.max_signal_position = self.antenna.get_max_signal_position()
        self.blackboard.antenna_position = self.max_signal_position

        path_max = self.pathfinder_service.find(self.global_information, self.max_signal_position)
        self.global_information.send_path([robot_position] + path_max)
        self.vision_regulation.go_to_positions(path_max)

        self.mark_move = self.blackboard.get_mark_move(robot_position)
        self.vision_regulation.oriente_robot(ANTENNA_DRAW_MARK_ANGLE)
        self.antenna.robot_controller.lower_pencil()
        self.antenna.robot_controller.timed_move(self.mark_move, 20, robot_position)
        self.antenna.robot_controller.raise_pencil()