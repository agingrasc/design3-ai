import math

import time

# from mcu.commands import Camera, Led
# from mcu.protocol import Leds
from robot.geometricinterpreter import geometric_interpreter
from robot.task.task import task

class take_picture(task):
    def __init__(self, robot_controller):
        task.__init__(self, robot_controller)
        self.next_state = self._take_image
        self.status_flag = 0
        self.robot_controller = None
        self.x_theta = -(math.pi/2)
        self.y_theta = -(math.pi/2)
        self.geometric_interpreter = geometric_interpreter()
        self.image = None

    def execute(self, x_robot_position, y_robot_position):
        print("taking image")
        print(self.id_image)
        print(self.magnification)
        print(self.orientation)

        self.next_state()
        return self.robot_controller

    def _take_image(self):
        # cmdCapture = Camera(self.x_theta, self.y_theta)
        # self.robot_controller.send_command(cmdCapture)
        #
        # cmd = Led(Leds.UP_GREEN)
        # self.send_command(cmd)
        # time.sleep(1)
        # cmd = Led(Leds.DOWN_GREEN)
        # self.send_command(cmd)

        self.next_state = self._analyse_picture

    def _analyse_picture(self):
        self.segments_image = self.geometric_interpreter.polygone_interpreter(self.image, self.orientation, self.magnification)

        if(len(self.segments_image) > 0):
            self.next_state = self._stop

    def _stop(self):
        self.status_flag = 1
