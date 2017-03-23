from domain.robot.task.task import Task
from domain.command.drawer import Drawer
from domain.robot.geometricinterpreter import GeometricInterpreter
from domain.robot.feedback import Feedback

MESSAGE = "End of drawing task!"


class DrawTask(Task):
    def __init__(self,
                 feedback: Feedback,
                 drawer: Drawer):
        super().__init__()
        self.drawer = drawer
        self.feedback = feedback

    def execute(self):
        self.drawer.draw(self.segments_image)
        self.feedback.send_comment(MESSAGE)
