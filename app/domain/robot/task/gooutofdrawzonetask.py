import math
import requests as req

# from mcu.commands import Led
# from mcu.protocol import Leds
# from mcu.commands import Move
from robot.task.task import Task


class GoOutOfDrawzoneTask(Task):
    def __init__(self, robot_controller):
        Task.__init__(self, robot_controller)
        self.x_safezone = 10
        self.y_safezone = 20
        self.x_robot_position = 10
        self.y_robot_position = 10
        self.theta = -(math.pi / 2)
        self.status_flag = 0

    def execute(self, x_robot_position, y_robot_position):
        print("quiting zone")
        self.y_robot_position = y_robot_position
        self.x_robot_position = x_robot_position
        self._quit_draw_zone()
        self._stop()

    def _quit_draw_zone(self):
        print("quiting")
        # for segment in self.segments_image:
        #     while self._distance(self.x_robot_position, self.y_robot_position, segment[0], segment[1]) <= 2:
        #         cmd = Move(segment[0], segment[1], self.theta)
        #         self.robot_controller.send_command(cmd)

    def _stop(self):
        self.status_flag = 1
        req.post(url=self.ROBOT_API_URL + "end-go-out-of-drawzone-task")