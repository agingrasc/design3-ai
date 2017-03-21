from unittest import TestCase
from unittest.mock import Mock, MagicMock, patch, call

from mcu.robotcontroller import RobotController
from robot.task.drawtask import DrawTask


class DrawTaskTest(TestCase):
    def test_execute_all_the_subtasks(self):
        x_robot_position = 10
        y_robot_position = 10
        robot_controler = Mock(RobotController)
        draw_task = DrawTask(robot_controler)

        mock = Mock()
        mock.draw_task._draw()
        mock.draw_task._stop()

        draw_task.execute(x_robot_position, y_robot_position)

        mock.draw_task._draw.assert_called_once()
        mock.draw_task._stop.assert_called_once()

    def test_task_status_change_to_done_at_the_end_of_execution(self):
        x_robot_position = 10
        y_robot_position = 10
        robot_controler = Mock(RobotController)
        draw_task = DrawTask(robot_controler)

        mock = Mock()
        mock.draw_task._stop()

        draw_task.execute(x_robot_position, y_robot_position)

        mock.draw_task._stop.assert_called_once()
        self.assertEquals(draw_task.status_flag, 1)

    def test_subtasks_are_executed_in_order(self):
        x_robot_position = 10
        y_robot_position = 10
        robot_controler = Mock(RobotController)
        draw_task = DrawTask(robot_controler)

        draw_mock = MagicMock()
        with patch('robot.task.drawtask.DrawTask._draw', draw_mock.function1), \
                patch('robot.task.drawtask.DrawTask._stop', draw_mock.function2):

            expected = [call.function1(), call.function2()]

            draw_task.execute(x_robot_position, y_robot_position)

            self.assertEqual(draw_mock.mock_calls, expected)
