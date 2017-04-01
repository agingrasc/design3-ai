from domain.robot.blackboard import Blackboard
from domain.robot.task.task import Task
from service.globalinformation import GlobalInformation


class TakePictureTask(Task):
    def __init__(self, global_information: GlobalInformation, blackboard: Blackboard):
        self.global_information = global_information
        self.blackboard = blackboard

    def execute(self):
        scale_factor = self.blackboard.magnification
        orientation = self.blackboard.orientation
        self.global_information.send_take_picture_request(scale_factor, orientation)
        print("Taking image: {} -- {} -- {}".format(self.blackboard.id_image, self.blackboard.orientation, self.blackboard.magnification))
