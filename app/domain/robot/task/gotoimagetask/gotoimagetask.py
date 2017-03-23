from domain.command.visionregulation import VisionRegulation
from domain.robot.feedback import Feedback
from domain.robot.task.task import Task
from domain.pathfinding import get_segments
from service.globalinformation import GlobalInformation
from service import pathfinding_application_service
from service.image_position_finder import ImagePositionFinder

class GoToImageTask(Task):
    def __init__(self, feedback: Feedback,
                        vision_regulation: VisionRegulation,
                        global_information: GlobalInformation,
                        pathfinding_application_service: pathfinding_application_service,
                        get_segments: get_segments,
                        image_position_finder: ImagePositionFinder):
        super().__init__()
        self.feedback = feedback
        self.vision_regulation = vision_regulation
        self.global_information = global_information
        self.pathfinding_application_service = pathfinding_application_service
        self.get_segments = get_segments
        self.image_position_finder = image_position_finder

    def execute(self):
        obstacles_list = self.global_information.get_obstacles()
        robot_position = self.global_information.get_robot_position()
        gameboard_width = self.global_information.get_gameboard_width()
        gameboard_length = self.global_information.get_gameboard_length()
        destination_position = self.image_position_finder.getImagePosition(self.id_image)
        path = self.pathfinding_application_service.find(obstacles_list, gameboard_width, gameboard_length, robot_position, destination_position[0])
        path_destinations = self.get_segments.get_filter_path(path)
        for destination in path_destinations:
            self.vision_regulation.go_to_position(destination)

        self.vision_regulation.oriente_robot(destination_position[1])
        self.feedback.send_comment("end of task going to image")

