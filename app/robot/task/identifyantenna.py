import math

from .task import task
# from mcu.commands import Move


class identify_antenna(task):
    def __init__(self):
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

    def execute(self):
        print("indentifying antenna")
        print(self.id_image)
        print(self.magnification)
        print(self.orientation)
        self.next_state()
        return self.robot_controller

    def _go_to_start_point(self):
        print("going to start point")
        print(self.x_start_point)
        print(self.y_start_point)
        # cmd = Move(self.x_start_point, self.y_start_point, self.theta)
        # self.robot_controller.send_command(cmd)

        # if cond:
        #     self.next_state = self._go_to_start_point
        # else:
        self.next_state = self._go_to_end_point


    def _go_to_end_point(self):
        print("goint to end point")
        print(self.x_end_point)
        print(self.y_end_point)
        # cmd = Move(self.x_end_point, self.y_end_point, self.theta)
        # self.robot_controller.send_command(cmd)
        self.next_state = self._go_to_max_point()

    def _go_to_max_point(self):
        print("going to max point")
        print(self.x_max_point)
        print(self.y_max_point)
        # cmd = Move(self.x_max_point, self.y_max_point, self.theta)
        # self.robot_controller.send_command(cmd)
        self.next_state = self._stop

    def _stop(self):
        self.status_flag = 1