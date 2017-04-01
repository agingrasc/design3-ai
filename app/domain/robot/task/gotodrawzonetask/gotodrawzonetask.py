from domain.command.visionregulation import VisionRegulation
from domain.robot.blackboard import Blackboard
from domain.robot.feedback import Feedback
from domain.robot.task.task import Task
from service.globalinformation import GlobalInformation
from service import pathfinding_application_service

DRAW_ANGLE = 45


class GoToDrawzoneTask(Task):
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
        first_point = self.blackboard.get_segments_image()[0]
        path = self.pathfinding_application_service.find(self.global_information, first_point)
        for destination in path:
            self.vision_regulation.go_to_position(destination)

        self.feedback.send_comment("end of task going to drawzone")
