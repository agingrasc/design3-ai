import math

from mcu.commands import Pencil
from mcu.protocol import PencilStatus
from .task import task
from mcu.commands import Move


class identify_antenna(task):
    def __init__(self):
        self.robot_controller = None
        task.__init__(self)
        self.x_start_point = 10
        self.y_start_point = 10
        self.x_end_point = 30
        self.y_end_point = 10
        self.x_max_point = 20
        self.y_max_point = 10
        self.theta = -(math.pi/2)
        self.next_state = self._go_to_start_point
        self.status_flag = 0
        self.x_robot_position = 10
        self.y_robot_position = 10

    def execute(self, x_robot_position, y_robot_position):
        print("indentifying antenna")
        print(self.id_image)
        print(self.magnification)
        print(self.orientation)
        self.x_robot_position = x_robot_position
        self.y_robot_position = y_robot_position
        self.next_state()
        return self.robot_controller

    def _go_to_start_point(self):
        print("going to start point")
        print(self.x_start_point)
        print(self.y_start_point)
        cmd = Move(self.x_start_point, self.y_start_point, self.theta)
        self.robot_controller.send_command(cmd)

        print(str(self._distance(self.x_robot_position, self.y_robot_position, self.x_start_point, self.y_end_point)))

        if self._distance(self.x_robot_position, self.y_robot_position, self.x_start_point, self.y_end_point) <= 2:
            self.next_state = self._go_to_end_point


    def _go_to_end_point(self):
        print("goint to end point")
        print(self.x_end_point)
        print(self.y_end_point)
        cmd = Move(self.x_end_point, self.y_end_point, self.theta)
        self.robot_controller.send_command(cmd)
        print(str(self._distance(self.x_robot_position, self.y_robot_position, self.x_end_point, self.y_end_point)))
        if self._distance(self.x_robot_position, self.y_robot_position, self.x_end_point, self.y_end_point) <= 2:
            self.next_state = self._go_to_max_point()

    def _go_to_max_point(self):
        print("going to max point")
        print(self.x_max_point)
        print(self.y_max_point)
        cmd = Move(self.x_max_point, self.y_max_point, self.theta)
        self.robot_controller.send_command(cmd)
        if self._distance(self.x_robot_position, self.y_robot_position, self.x_max_point, self.y_max_point) <= 2:
            self.next_state = self._mark_antenna

    def _mark_antenna(self):
        print("mariking antenna")
        cmdPencil = Pencil(PencilStatus.RAISED)
        self.robot_controller.send_command(cmdPencil)

        while self._distance(self.y_robot_position, self.y_robot_position, self.x_robot_position, (self.y_robot_position + 5)) > 1:
            cmd = Move(self.x_robot_position, (self.y_robot_position + 5), self.theta)
            self.robot_controller.send_command(cmd)

        cmdPencil = Pencil(PencilStatus.LOWERED)
        self.robot_controller.send_command(cmdPencil)

        self.next_state = self._stop

    def _stop(self):
        self.status_flag = 1