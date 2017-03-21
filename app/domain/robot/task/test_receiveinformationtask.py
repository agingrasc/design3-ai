from unittest import TestCase
from unittest.mock import Mock, MagicMock, patch, call

from mcu.robotcontroller import RobotController
from robot.task.receiveinformationtask import ReceiveInformationTask


class ReceiveInformationsTaskTest(TestCase):

    def test_execute_all_the_subtasks(self):
        x_robot_position =  10
        y_robot_position = 10
        robot_controler = Mock(RobotController)
        receive_information_task = ReceiveInformationTask(robot_controler)

        mock = Mock()
        mock.receive_information_task._get_information()
        mock.receive_information_task._stop()

        receive_information_task.execute(x_robot_position, y_robot_position)

        mock.receive_information_task._get_information.assert_called_once()
        mock.receive_information_task._stop.assert_called_once()

    def test_task_status_change_to_done_at_the_end_of_execution(self):
        x_robot_position = 10
        y_robot_position = 10
        robot_controler = Mock(RobotController)
        receive_information_task = ReceiveInformationTask(robot_controler)

        mock = Mock()
        mock.receive_information_task._stop()

        receive_information_task.execute(x_robot_position, y_robot_position)

        mock.receive_information_task._stop.assert_called_once()
        self.assertEquals(receive_information_task.status_flag, 1)

    def test_subtasks_are_executed_in_order(self):
        x_robot_position = 10
        y_robot_position = 10
        robot_controler = Mock(RobotController)
        receive_information_task = ReceiveInformationTask(robot_controler)

        receive_information_mock = MagicMock()
        with patch('robot.task.receiveinformationtask.ReceiveInformationTask._get_information', receive_information_mock.function1), \
                patch('robot.task.receiveinformationtask.ReceiveInformationTask._stop', receive_information_mock.function2):

            expected = [
                call.function1(),
                call.function2()
            ]

            receive_information_task.execute(x_robot_position, y_robot_position)
            self.assertEqual(receive_information_mock.mock_calls, expected)

