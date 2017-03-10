import math

from mcu.commands import Led
from mcu.protocol import Leds
from mcu.commands import Move
from robot.task.task import task


class end_cycle(task):
    def __init__(self, robot_controller):
        task.__init__(self, robot_controller)
        self.x_safezone = 10
        self.y_safezone = 20
        self.x_robot_position = 10
        self.y_robot_position = 10
        self.theta = -(math.pi / 2)
        self.next_state = self._quit_draw_zone
        self.status_flag = 0
        self.robot_controller = None

    def execute(self, x_robot_position, y_robot_position):
        print("quiting zone")
        print(self.id_image)
        print(self.magnification)
        print(self.orientation)
        self.y_robot_position = y_robot_position
        self.x_robot_position = x_robot_position
        self.next_state()
        return self.robot_controller

    def _quit_draw_zone(self):
        print("quiting")
        for segment in self.segments_image:
            while self._distance(self.x_robot_position, self.y_robot_position, segment[0], segment[1]) <= 2:
                cmd = Move(segment[0], segment[1], self.theta)
                self.robot_controller.send_command(cmd)

        if self._distance(self.x_robot_position, self.y_robot_position, self.x_safezone, self.y_safezone) <= 2:
            self.next_state = self._launch_end_signal

    def _launch_end_signal(self):
        print("Red led")

        cmd = Led(Leds.UP_RED)
        self.robot_controller.send_command(cmd)

        self.next_state = self._stop

    def _stop(self):
        self.status_flag = 1