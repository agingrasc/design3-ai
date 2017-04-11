from domain.command.visionregulation import VisionRegulation
from domain.robot.blackboard import Blackboard
from domain.robot.task.task import Task
from service import pathfinding_application_service
from service.feedback import Feedback
from service.feedback import TASK_GO_TO_DRAWING_ZONE
from service.globalinformation import GlobalInformation

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
        robot_position = self.global_information.get_robot_position()
        segments = self.blackboard.get_image_segments()
        first_point = segments[0]
        path = self.pathfinding_application_service.find(self.global_information, first_point)
        self.global_information.send_path([robot_position] + path)
        for destination in path:
            self.vision_regulation.oriente_robot(destination.theta)
            self.vision_regulation.go_to_position(destination)

        self.feedback.send_comment(TASK_GO_TO_DRAWING_ZONE)
