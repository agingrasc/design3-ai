import time

from domain.robot.blackboard import Blackboard
from domain.robot.task.task import Task
from service.globalinformation import GlobalInformation
from service.feedback import Feedback
from service.feedback import TASK_TAKE_PICTURE

CAMERA_STABILIZING_SLEEP_TIME = 5


class TakePictureTask(Task):
    def __init__(self, global_information: GlobalInformation, blackboard: Blackboard, feedback: Feedback):
        self.global_information = global_information
        self.blackboard = blackboard
        self.feedback = feedback

    def execute(self):
        time.sleep(CAMERA_STABILIZING_SLEEP_TIME)
        scale_factor = self.blackboard.magnification
        orientation = self.blackboard.orientation
        self.global_information.send_take_picture_request(scale_factor, orientation)
        print(
            "Taking image: {} -- {} -- {}".
            format(self.blackboard.id_image, self.blackboard.orientation, self.blackboard.magnification)
        )
        self.feedback.send_comment(TASK_TAKE_PICTURE)
