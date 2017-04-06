from unittest import TestCase
from unittest.mock import Mock

from domain.robot.task.shutdownredledtask.shutdownredledtask import ShutDownRedLedTask


class ShutDownRedLedTaskTest(TestCase):
    def setUp(self):
        self.feedback = Mock()
        self.lighter = Mock()

    def test_send_feedback(self):
        task = ShutDownRedLedTask(self.feedback, self.lighter)

        task.execute()


        self.feedback.send_new_cycle.assert_called_once()

    def test_shut_down_red_led(self):
        task = ShutDownRedLedTask(self.feedback, self.lighter)

        task.execute()

        self.lighter.shut_down_red_led.assert_called_once()
