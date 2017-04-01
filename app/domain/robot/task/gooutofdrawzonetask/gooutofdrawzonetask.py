from domain.command.visionregulation import VisionRegulation
from domain import pathfinding
from domain.robot.task.task import Task
from service import pathfinding_application_service
from service.destinationcalculator import DestinationCalculator
from service.feedback import Feedback
from service.globalinformation import GlobalInformation


class GoOutOfDrawzoneTask(Task):
    def __init__(
        self,
        feedback: Feedback,
        vision_regulation: VisionRegulation,
        destination_calculator: DestinationCalculator,
        global_information: GlobalInformation
    ):
        self.feedback = feedback
        self.vision_regulation = vision_regulation
        self.destination_calculator = destination_calculator
        self.global_information = global_information
        self.pathfinder_service = pathfinding_application_service
        self.get_segments = pathfinding.get_segments

    def execute(self):
        obstacles = self.global_information.get_obstacles()
        robot_position = self.global_information.get_robot_position()
        safezone_position = self.destination_calculator.get_safezone(obstacles, robot_position)
        path = self.pathfinder_service.find(self.global_information, safezone_position)
        self.vision_regulation.go_to_positions(path)

        self.feedback.send_comment("End going to safezone.")
