import math
import requests as req

# from mcu.commands import Camera, Led
# from mcu.protocol import Leds
from domain.robot.blackboard import Blackboard
from domain.robot.geometricinterpreter import GeometricInterpreter
from domain.robot.task.task import Task


class TakePictureTask(Task):
    def __init__(self, blackboard: Blackboard):
        self.blackboard = blackboard

    def execute(self):
        print("Taking image: {} -- {} -- {}".format(self.blackboard.id_image, self.blackboard.orientation, self.blackboard.magnification))
