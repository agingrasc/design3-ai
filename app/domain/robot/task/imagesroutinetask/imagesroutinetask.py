from domain.command.visionregulation import VisionRegulation
from domain.robot.blackboard import Blackboard
from domain.robot.task.task import Task
from service.globalinformation import GlobalInformation


class ImagesRoutineTask(Task):
    def __init__(self, global_information: GlobalInformation, blackboard: Blackboard, vision_regulation: VisionRegulation):

        self.global_information = global_information
        self.blackboard = blackboard
        self.vision_regulation = vision_regulation


    def execute(self):
        for position in self.blackboard.images_position.values():
            self.vision_regulation.go_to_position(position)
            self.global_information.send_take_picture_request(0.5, "SOUTH")