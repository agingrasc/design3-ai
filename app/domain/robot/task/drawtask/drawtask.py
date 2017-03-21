from domain.robot.task.task import Task
from domain.command.drawer import Drawer
from mcu.robotcontroller import RobotController
from domain.robot.geometricinterpreter import GeometricInterpreter
from domain.robot.feedback import Feedback

MESSAGE = "End of drawing task!"


class DrawTask(Task):
    def __init__(self,
                 feedback: Feedback,
                 drawer: Drawer,
                 geometricinterpreter: GeometricInterpreter):
        self.geometricinterpreter = geometricinterpreter
        self.drawer = drawer
        self.feedback = feedback

    def execute(self):
        picture_corners = self.geometricinterpreter.polygone_interpreter()
        self.drawer.draw(picture_corners)
        self.feedback.send_comment(MESSAGE)
