from domain.command.visionregulation import VisionRegulation
from domain.pathfinding import get_segments
from domain.robot.feedback import Feedback
from domain.robot.task.task import Task
from service import pathfinding_application_service
from service.destinationcalculator import DestinationCalculator
from service.globalinformation import GlobalInformation

WIDTH_TABLE = 1120
LENGTH_TABLE = 2300

class GoOutOfDrawzoneTask(Task):
    def __init__(self, feedback: Feedback,
                        vision_regulation: VisionRegulation,
                        destination_calculator: DestinationCalculator,
                        global_information: GlobalInformation):
        self.feedback = feedback
        self.vision_regulation = vision_regulation
        self.destination_calculator = destination_calculator
        self.global_information = global_information

    def execute(self):
        obstacles = self.global_information.get_obstacles()
        robot_position = self.global_information.get_robot_position()
        safezone_position = self.destination_calculator.get_safezone(obstacles, robot_position)
        path = pathfinding_application_service.find(obstacles, WIDTH_TABLE, LENGTH_TABLE, robot_position, safezone_position)
        path = get_segments.get_filter_path(path)
        for destination in path:
            self.vision_regulation.go_to_position(destination)

        self.feedback.send_comment("end going to safezone")

