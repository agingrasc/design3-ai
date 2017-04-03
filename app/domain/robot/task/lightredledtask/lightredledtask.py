from domain.command.lighter import Lighter
from domain.robot.task.task import Task

from service.feedback import Feedback


class LightRedLedTask(Task):
    def __init__(self, feedback: Feedback, lighter: Lighter):
        self.feedback = feedback
        self.lighter = lighter

    def execute(self):
        self.lighter.light_red_led()
        self.feedback.send_comment(self.feedback.TASK_LIGHT_RED_LED)
