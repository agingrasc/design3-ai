from typing import Dict

from domain.command.visionregulation import VisionRegulation
from domain.gameboard.position import Position
from domain.pathfinding import get_segments
from domain.robot.blackboard import Blackboard
from domain.robot.task.task import Task
from service.globalinformation import GlobalInformation
from service import pathfinding_application_service
from service.feedback import Feedback
from service.feedback import TASK_GO_TO_IMAGE
from service.globalinformation import GlobalInformation

images_position: Dict[int, Position] = {
    0: Position(1959, 366, 1.57),
    1: Position(2024, 305, 1.22),
    2: Position(1933, 267, 0.35),
    3: Position(1933, 267, 0),
    4: Position(1929, 615, 0),
    5: Position(1895, 842, 0),
    6: Position(2096, 551, -1.37),
    7: Position(1925, 657, -1.57)
}


class GoToImageTask(Task):
    def __init__(
        self,
        feedback: Feedback,
        vision_regulation: VisionRegulation,
        global_information: GlobalInformation,
        pathfinder_service: pathfinding_application_service,
        blackboard: Blackboard
    ):
        super().__init__()
        self.feedback = feedback
        self.vision_regulation = vision_regulation
        self.global_information = global_information
        self.pathfinding_application_service = pathfinder_service
        self.blackboard = blackboard

    def execute(self):
        image_position = images_position[self.blackboard.get_image_id()]
        path = self.pathfinding_application_service.find(self.global_information, image_position)
        for destination in path:
            self.vision_regulation.go_to_position(destination)

        self.vision_regulation.oriente_robot(image_position.theta)
        self.feedback.send_comment(TASK_GO_TO_IMAGE)
