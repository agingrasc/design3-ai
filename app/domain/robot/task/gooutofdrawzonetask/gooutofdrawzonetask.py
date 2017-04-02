from domain.command.visionregulation import VisionRegulation
from domain.gameboard.position import Position
from domain.robot.task.task import Task
from service import pathfinding_application_service
from service.feedback import Feedback
from service.globalinformation import GlobalInformation

STOP_POSITION = Position(1250, 880, 0)  # 1280, 865


class GoOutOfDrawzoneTask(Task):
    def __init__(self, feedback: Feedback, vision_regulation: VisionRegulation, global_information: GlobalInformation):
        self.feedback = feedback
        self.vision_regulation = vision_regulation
        self.global_information = global_information
        self.pathfinder_service = pathfinding_application_service

    def execute(self):
        safezone_position = STOP_POSITION
        path = self.pathfinder_service.find(self.global_information, safezone_position)
        self.vision_regulation.go_to_positions(path)

        self.feedback.send_comment("End going to safezone.")
