import numpy as np

from domain.command.visionregulation import VisionRegulation
from domain.gameboard.position import Position
from domain.robot.feedback import Feedback
from domain.robot.task.task import Task
from domain.pathfinding import get_segments
from service.globalinformation import GlobalInformation
from service import pathfinding_application_service

DRAWZONE_POSITION = Position(300, 250)
DRAW_ANGLE = 45


class GoToDrawzoneTask(Task):
    def __init__(self,
                 feedback: Feedback,
                 vision_regulation: VisionRegulation,
                 global_information: GlobalInformation,
                 pathfinding_application_service: pathfinding_application_service):
        super().__init__()
        self.feedback = feedback
        self.vision_regulation = vision_regulation
        self.global_information = global_information
        self.pathfinding_application_service = pathfinding_application_service

    def execute(self):
        path = self.pathfinding_application_service.find(self.global_information, DRAWZONE_POSITION)
        for destination in path:
            self.vision_regulation.go_to_position(destination)

        self.feedback.send_comment("end of task going to drawzone")



