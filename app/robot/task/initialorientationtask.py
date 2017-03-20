from robot.task.task import Task


class InitialOrientationTask(Task):
    def __init__(self, robot_controller):
        Task.__init__(self, robot_controller)
        self.status_flag = 0

    def execute(self, x_robot_position, y_robot_position):
        print("orienting the robot")
        self._set_initial_orientation()
        self._stop()

    def _set_initial_orientation(self):
        print("Orientation is changing")
        # cmd = Led(Leds.UP_RED)
        # self.robot_controller.send_command(cmd)