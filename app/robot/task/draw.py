import math

from mcu.commands import Move
from mcu.commands import Pencil
from mcu.protocol import PencilStatus
from robot.task.task import task


class draw(task):
    def __init__(self, robot_controller):
        task.__init__(self, robot_controller)
        self.x_robot_position = 20
        self.y_robot_position = 40
        self.theta = -(math.pi / 2)
        self.next_state = self._draw
        self.status_flag = 0
        self.robot_controller = None

    def execute(self, x_robot_position, y_robot_position):
        print("drawing")
        print(self.id_image)
        print(self.magnification)
        print(self.orientation)
        self.y_robot_position = y_robot_position
        self.x_robot_position = x_robot_position
        self.next_state()
        return self.robot_controller

    def _draw(self):
        print("in draw")
        cmdPencil = Pencil(PencilStatus.RAISED)
        self.robot_controller.send_command(cmdPencil)

        for segment in self.segments_image:
            while self._distance(self.x_robot_position, self.y_robot_position, segment[0], segment[1]) <= 2:
                cmd = Move(segment[0], segment[1], self.theta)
                self.robot_controller.send_command(cmd)

        cmdPencil = Pencil(PencilStatus.LOWERED)
        self.robot_controller.send_command(cmdPencil)

        if self._distance(self.x_robot_position, self.y_robot_position, self.segments_image[len(self.segments_image)-1][0],
                          self.segments_image[len(self.segments_image)-1][1]) <= 2:
            self.next_state = self._stop

    def _stop(self):
        self.status_flag = 1