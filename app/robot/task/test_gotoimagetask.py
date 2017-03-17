from unittest import TestCase
from unittest.mock import Mock, MagicMock, patch, call

from domain.gameboard.gameboard import GameBoard
from mcu.robotcontroller import RobotController
from robot.task.gotoimagetask import GoToImageTask
from domain.pathfinding import pathfinding


class GoToImageTaskTest(TestCase):

    def test_execute_all_the_subtasks(self):
        x_robot_position = 10
        y_robot_position = 10
        robot_controler = Mock(RobotController)
        go_to_image_task = GoToImageTask(robot_controler)

        mock = Mock()
        mock.go_to_image_task._find_path()
        mock.go_to_image_task._go_to_image()
        mock.go_to_image_task._stop()

        go_to_image_task.execute(x_robot_position, y_robot_position)

        mock.go_to_image_task._find_path.assert_called_once()
        mock.go_to_image_task._go_to_image.assert_called_once()
        mock.go_to_image_task._stop.assert_called_once()

    def test_task_status_change_to_done_at_the_end_of_execution(self):
        x_robot_position = 10
        y_robot_position = 10
        robot_controler = Mock(RobotController)
        go_to_image_task = GoToImageTask(robot_controler)

        mock = Mock()
        mock.go_to_image_task._stop()

        go_to_image_task.execute(x_robot_position, y_robot_position)

        mock.go_to_image_task._stop.assert_called_once()
        self.assertEquals(go_to_image_task.status_flag, 1)

    def test_subtasks_are_executed_in_order(self):
        x_robot_position = 10
        y_robot_position = 10
        robot_controler = Mock(RobotController)
        go_to_image_task = GoToImageTask(robot_controler)

        go_to_image_mock = MagicMock()
        with patch('robot.task.gotoimagetask.GoToImageTask._find_path', go_to_image_mock.function1), \
                patch('robot.task.gotoimagetask.GoToImageTask._go_to_image', go_to_image_mock.function2), \
                patch('robot.task.gotoimagetask.GoToImageTask._stop', go_to_image_mock.function3):

            expected = [
                call.function1(),
                call.function2(),
                call.function3()
            ]

            go_to_image_task.execute(x_robot_position, y_robot_position)

            self.assertEqual(go_to_image_mock.mock_calls, expected)