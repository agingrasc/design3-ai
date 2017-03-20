import requests as req

# from mcu.commands import Led
# from mcu.protocol import Leds
from robot.task.task import Task


class LightRedLedTask(Task):
    def __init__(self, robot_controller):
        Task.__init__(self, robot_controller)
        self.status_flag = 0

    def execute(self, x_robot_position, y_robot_position):
        print("lighting red led")
        self._launch_end_signal()
        self._stop()

    def _launch_end_signal(self):
        print("Red led")
        # cmd = Led(Leds.UP_RED)
        # self.robot_controller.send_command(cmd)

    def _stop(self):
        self.status_flag = 1
        req.post(url=self.ROBOT_API_URL + "end-light-red-led-task")