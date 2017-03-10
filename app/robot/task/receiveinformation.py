from robot.task.task import task


class receive_information(task):
    def __init__(self, robot_controller):
        task.__init__(self, robot_controller)
        self.next_state = self._get_information
        self.status_flag = 0
        self.robot_controller = None

    def execute(self, x_robot_position, y_robot_position):
        print("receiving information")
        self.next_state()
        return self.robot_controller

    def _get_information(self):
        print("getting information")
        # place where to add the command to get the information and set the in the right variable

        self.next_state = self._stop

    def _stop(self):
        self.status_flag = 1