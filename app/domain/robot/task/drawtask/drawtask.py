from domain.robot.blackboard import Blackboard
from domain.robot.task.task import Task
from domain.command.drawer import Drawer
from service.feedback import Feedback
from service.globalinformation import GlobalInformation
from service.feedback import TASK_DRAW_IMAGE


class DrawTask(Task):
    def __init__(self, feedback: Feedback, drawer: Drawer, global_information: GlobalInformation, blackboard: Blackboard):
        super().__init__()
        self.drawer = drawer
        self.feedback = feedback
        self.global_information = global_information
        self.blackboard = blackboard

    def execute(self):
        draw_path = self.blackboard.get_image_segments()
        self.global_information.send_path(draw_path)
        self.drawer.draw(draw_path)
        self.feedback.send_comment(TASK_DRAW_IMAGE)