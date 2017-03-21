import requests as req

from robot.task.task import Task


class ReceiveInformationTask(Task):
    def __init__(self, robot_controller):
        Task.__init__(self, robot_controller)
        self.status_flag = 0

    def execute(self, x_robot_position, y_robot_position):
        print("receiving information")
        self._get_information()
        self._stop()

    def _get_information(self):
        print("getting information")
        # place where to add the command to get the information and set the in the right variable

    def _stop(self):
        self.status_flag = 1
        req.post(url=self.ROBOT_API_URL + "end-receive-information-task")