from unittest import TestCase
from unittest.mock import Mock, MagicMock, patch, call

from mcu.robotcontroller import RobotController
from robot.task.initialorientationtask import InitialOrientationTask


class InitialOrientationTaskTest(TestCase):

    def test_execute_all_the_subtasks(self):
        x_robot_position = 10
        y_robot_position = 10
        robot_controler = Mock(RobotController)
        initial_orientation_task = InitialOrientationTask(robot_controler)

        mock = Mock()
        mock.initial_orientation_task._set_initial_orientation()
        mock.initial_orientation_task._stop()

        initial_orientation_task.execute(x_robot_position, y_robot_position)

        mock.initial_orientation_task._set_initial_orientation.assert_called_once()
        mock.initial_orientation_task._stop.assert_called_once()

    def test_task_status_change_to_done_at_the_end_of_execution(self):
        x_robot_position = 10
        y_robot_position = 10
        robot_controler = Mock(RobotController)
        initial_orientation_task = InitialOrientationTask(robot_controler)

        mock = Mock()
        mock.initial_orientation_task._stop()

        initial_orientation_task.execute(x_robot_position, y_robot_position)

        mock.initial_orientation_task._stop.assert_called_once()
        self.assertEquals(initial_orientation_task.status_flag, 1)

    def test_subtasks_are_executed_in_order(self):
        x_robot_position = 10
        y_robot_position = 10
        robot_controler = Mock(RobotController)
        initial_orientation_task = InitialOrientationTask(robot_controler)

        initial_orientation_mock = MagicMock()
        with patch('robot.task.initialorientationtask.InitialOrientationTask._set_initial_orientation', initial_orientation_mock.function1), \
                patch('robot.task.initialorientationtask.InitialOrientationTask._stop', initial_orientation_mock.function2):

            expected = [
                call.function1(),
                call.function2()
            ]

            initial_orientation_task.execute(x_robot_position, y_robot_position)

            self.assertEqual(initial_orientation_mock.mock_calls, expected)