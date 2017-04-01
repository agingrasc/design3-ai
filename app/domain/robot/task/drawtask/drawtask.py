from domain.command.drawer import Drawer
from domain.robot.blackboard import Blackboard
from domain.robot.task.task import Task
from service.feedback import Feedback

MESSAGE = "End of drawing task!"


class DrawTask(Task):
    def __init__(self,
                 feedback: Feedback,
                 drawer: Drawer,
                 blackboard: Blackboard):
        super().__init__()
        self.drawer = drawer
        self.feedback = feedback
        self.blackboard = blackboard

    def execute(self):
        self.drawer.draw(self.blackboard.segments_image)
        self.feedback.send_comment(MESSAGE)
