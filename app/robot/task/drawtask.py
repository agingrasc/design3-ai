import math

# from mcu.commands import Move
# from mcu.commands import Pencil
from mcu.protocol import PencilStatus
from robot.task.task import Task


class DrawTask(Task):
    def __init__(self, robot_controller):
        Task.__init__(self, robot_controller)
        self.x_robot_position = 20
        self.y_robot_position = 40
        self.theta = -(math.pi / 2)
        self.status_flag = 0

    def execute(self, x_robot_position, y_robot_position):
        print("drawing")
        print(self.id_image)
        print(self.magnification)
        print(self.orientation)
        self.y_robot_position = y_robot_position
        self.x_robot_position = x_robot_position
        self._draw()
        self._stop()

    def _draw(self):
        print("in draw")
        # cmdPencil = Pencil(PencilStatus.RAISED)
        # self.robot_controller.send_command(cmdPencil)
        #
        # for segment in self.segments_image:
        #     while self._distance(self.x_robot_position, self.y_robot_position, segment[0], segment[1]) <= 2:
        #         cmd = Move(segment[0], segment[1], self.theta)
        #         self.robot_controller.send_command(cmd)
        #
        # cmdPencil = Pencil(PencilStatus.LOWERED)
        # self.robot_controller.send_command(cmdPencil)