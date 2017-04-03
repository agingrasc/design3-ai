from unittest import TestCase
from unittest.mock import Mock

from domain.robot.task.lightredledtask.lightredledtask import LightRedLedTask


class LightRedLedTaskTest(TestCase):
    def setUp(self):
        self.feedback = Mock()
        self.lighter = Mock()

    def test_send_feedback(self):
        task = LightRedLedTask(self.feedback, self.lighter)

        task.execute()

        self.feedback.send_comment.assert_called_once()

    def test_light_red_led(self):
        task = LightRedLedTask(self.feedback, self.lighter)

        task.execute()

        self.lighter.light_red_led.assert_called_once()
