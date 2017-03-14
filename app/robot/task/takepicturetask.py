import math

import time

from mcu.commands import Camera, Led
from mcu.protocol import Leds
from robot.geometricinterpreter import GeometricInterpreter
from robot.task.task import Task

class TakePictureTask(Task):
    def __init__(self, robot_controller):
        Task.__init__(self, robot_controller)
        self.status_flag = 0
        self.x_theta = -(math.pi/2)
        self.y_theta = -(math.pi/2)
        self.geometric_interpreter = GeometricInterpreter()
        self.image = None

    def execute(self, x_robot_position, y_robot_position):
        print("taking image")
        print(self.id_image)
        print(self.magnification)
        print(self.orientation)
        self._take_image()
        self._analyse_picture()
        self._stop()
        return self.robot_controller

    def _take_image(self):
        cmdCapture = Camera(self.x_theta, self.y_theta)
        self.robot_controller.send_command(cmdCapture)

        # place to add the command capture image

        cmd = Led(Leds.UP_GREEN)
        self.robot_controller.send_command(cmd)
        time.sleep(1)
        cmd = Led(Leds.DOWN_GREEN)
        self.robot_controller.send_command(cmd)

    def _analyse_picture(self):
        self.segments_image = self.geometric_interpreter.polygone_interpreter(self.image, self.orientation, self.magnification)

    def _stop(self):
        self.status_flag = 1
