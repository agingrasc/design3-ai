from domain.command.visionregulation import VisionRegulation
from domain.gameboard.position import Position
from domain.robot.feedback import Feedback
from domain.robot.task.task import Task
from domain.pathfinding import get_segments
from service.globalinformation import GlobalInformation
from service import pathfinding_application_service


images_position = {0: Position(1959, 366, 1.57),
                   1: Position(2024, 305, 1.22),
                   2: Position(1933, 267, 0.35),
                   3: Position(1933, 267, -0.17),
                   4: Position(1929, 615, 0),
                   5: Position(1895, 842, 0),
                   6: Position(2096, 551, -1.57),
                   7: Position(1925, 657, -1.57)}


class GoToImageTask(Task):
    def __init__(self,
                 feedback: Feedback,
                 vision_regulation: VisionRegulation,
                 global_information: GlobalInformation,
                 pathfinding_application_service: pathfinding_application_service,
                 get_segments: get_segments):
        super().__init__()
        self.feedback = feedback
        self.vision_regulation = vision_regulation
        self.global_information = global_information
        self.pathfinding_application_service = pathfinding_application_service
        self.get_segments = get_segments

    def execute(self):
        robot_position = self.global_information.get_robot_position()
        path = self.pathfinding_application_service.find()
        path_destinations = self.get_segments.get_filter_path(path)
        for destination in path_destinations:
            self.vision_regulation.go_to_position(destination)

        self.vision_regulation.oriente_robot(destination_position[1])
        self.feedback.send_comment("end of task going to image")

