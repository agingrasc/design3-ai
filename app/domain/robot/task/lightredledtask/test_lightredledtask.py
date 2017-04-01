from unittest import TestCase
from unittest.mock import Mock, MagicMock, patch, call

from mcu.robotcontroller import RobotController
from robot.task.lightredledtask import LightRedLedTask


class LightRedLedTaskTest(TestCase):

    def test_execute_all_the_subtasks(self):
        x_robot_position = 10
        y_robot_position = 10
        robot_controler = Mock(RobotController)
        light_red_led_task = LightRedLedTask(robot_controler)

        mock = Mock()
        mock.light_red_led_task._launch_end_signal()
        mock.light_red_led_task._stop()

        light_red_led_task.execute(x_robot_position, y_robot_position)

        mock.light_red_led_task._launch_end_signal.assert_called_once()
        mock.light_red_led_task._stop.assert_called_once()

    def test_task_status_change_to_done_at_the_end_of_execution(self):
        x_robot_position = 10
        y_robot_position = 10
        robot_controler = Mock(RobotController)
        light_red_led_task = LightRedLedTask(robot_controler)

        mock = Mock()
        mock.light_red_led_task._stop()

        light_red_led_task.execute(x_robot_position, y_robot_position)

        mock.light_red_led_task._stop.assert_called_once()
        self.assertEquals(light_red_led_task.status_flag, 1)

    def test_subtasks_are_executed_in_order(self):
        x_robot_position = 10
        y_robot_position = 10
        robot_controler = Mock(RobotController)
        light_red_led_task = LightRedLedTask(robot_controler)

        light_red_led_mock = MagicMock()
        with patch('robot.task.lightredledtask.LightRedLedTask._launch_end_signal', light_red_led_mock.function1), \
                patch('robot.task.lightredledtask.LightRedLedTask._stop', light_red_led_mock.function2):

            expected = [
                call.function1(),
                call.function2()
            ]

            light_red_led_task.execute(x_robot_position, y_robot_position)

            self.assertEqual(light_red_led_mock.mock_calls, expected)