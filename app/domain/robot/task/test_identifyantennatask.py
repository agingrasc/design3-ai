from unittest import TestCase
from unittest.mock import Mock, MagicMock, patch, call

from mcu.robotcontroller import RobotController
from robot.task.identifyantennatask import IdentifyAntennaTask


class IdentifyAntennaTaskTest(TestCase):

    def test_execute_all_the_subtasks(self):
        x_robot_position =  10
        y_robot_position = 10
        robot_controler = Mock(RobotController)
        identify_antenna_task = IdentifyAntennaTask(robot_controler)

        mock = Mock()
        mock.identify_antenna_task._go_to_start_point()
        mock.identify_antenna_task._go_to_end_point()
        mock.identify_antenna_task._go_to_max_point()
        mock.identify_antenna_task._mark_antenna()
        mock.identify_antenna_task._stop()

        identify_antenna_task.execute(x_robot_position, y_robot_position)

        mock.identify_antenna_task._go_to_start_point.assert_called_once()
        mock.identify_antenna_task._go_to_end_point.assert_called_once()
        mock.identify_antenna_task._go_to_max_point.assert_called_once()
        mock.identify_antenna_task._mark_antenna.assert_called_once()
        mock.identify_antenna_task._stop.assert_called_once()

    def test_task_status_change_to_done_at_the_end_of_execution(self):
        x_robot_position = 10
        y_robot_position = 10
        robot_controler = Mock(RobotController)
        identify_antenna_task = IdentifyAntennaTask(robot_controler)

        mock = Mock()
        mock.identify_antenna_task._stop()

        identify_antenna_task.execute(x_robot_position, y_robot_position)

        mock.identify_antenna_task._stop.assert_called_once()
        self.assertEquals(identify_antenna_task.status_flag, 1)

    def test_subtasks_are_executed_in_order(self):
        x_robot_position = 10
        y_robot_position = 10
        robot_controler = Mock(RobotController)
        identify_antenna_task = IdentifyAntennaTask(robot_controler)

        identify_antenna_mock = MagicMock()
        with patch('robot.task.identifyantennatask.IdentifyAntennaTask._go_to_start_point', identify_antenna_mock.function1), \
                patch('robot.task.identifyantennatask.IdentifyAntennaTask._go_to_end_point', identify_antenna_mock.function2), \
                patch('robot.task.identifyantennatask.IdentifyAntennaTask._go_to_max_point', identify_antenna_mock.function3),\
                patch('robot.task.identifyantennatask.IdentifyAntennaTask._mark_antenna', identify_antenna_mock.function4), \
                patch('robot.task.identifyantennatask.IdentifyAntennaTask._stop', identify_antenna_mock.function5):

            expected = [
                call.function1(),
                call.function2(),
                call.function3(),
                call.function4(),
                call.function5()
            ]

            identify_antenna_task.execute(x_robot_position, y_robot_position)
            self.assertEqual(identify_antenna_mock.mock_calls, expected)





