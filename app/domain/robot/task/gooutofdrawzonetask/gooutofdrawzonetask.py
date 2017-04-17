from domain.command.visionregulation import VisionRegulation
from domain.gameboard.position import Position
from domain.robot.task.task import Task
from service.feedback import Feedback
from service.feedback import TASK_GO_OUT_OF_DRAWING_ZONE
from service.globalinformation import GlobalInformation
from service.safezonefinder import SafeZoneFinder

STOP_POSITION = Position(1250, 880, 0)  # 1280, 865


class GoOutOfDrawzoneTask(Task):
    def __init__(
        self,
        feedback: Feedback,
        vision_regulation: VisionRegulation,
        global_information: GlobalInformation,
        safe_zone_finder: SafeZoneFinder
    ):
        self.feedback = feedback
        self.vision_regulation = vision_regulation
        self.global_information = global_information
        self.safe_zone_finder = safe_zone_finder

    def execute(self):
        safe_zone_path = self.safe_zone_finder.find_safe_zone()
        robot_position = self.global_information.get_robot_position()
        self.global_information.send_path([robot_position] + safe_zone_path)
        self.vision_regulation.go_to_positions(safe_zone_path)
        self.feedback.send_comment(TASK_GO_OUT_OF_DRAWING_ZONE)
