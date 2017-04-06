from domain.robot.blackboard import Blackboard
from domain.robot.task.task import Task
from domain.command.drawer import Drawer
from service.feedback import Feedback
from service.feedback import TASK_DRAW_IMAGE

MESSAGE = "End of drawing task!"


class DrawTask(Task):
    def __init__(self, feedback: Feedback, drawer: Drawer, blackboard: Blackboard):
        super().__init__()
        self.drawer = drawer
        self.feedback = feedback
        self.blackboard = blackboard

    def execute(self):
        self.drawer.draw(self.blackboard.get_image_segments())
        self.feedback.send_comment(TASK_DRAW_IMAGE)
