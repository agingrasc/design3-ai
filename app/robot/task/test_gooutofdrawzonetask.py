from unittest import TestCase
from unittest.mock import Mock, MagicMock, patch, call

from mcu.robotcontroller import RobotController
from robot.task.gooutofdrawzonetask import GoOutOfDrawzoneTask


class GoOutOfDrawzoneTaskTest(TestCase):

    def test_execute_all_the_subtasks(self):
        x_robot_position = 10
        y_robot_position = 10
        robot_controler = Mock(RobotController)
        go_out_of_drawzone_task = GoOutOfDrawzoneTask(robot_controler)

        mock = Mock()
        mock.go_out_of_drawzone_task._quit_draw_zone()
        mock.go_out_of_drawzone_task._stop()

        go_out_of_drawzone_task.execute(x_robot_position, y_robot_position)

        mock.go_out_of_drawzone_task._quit_draw_zone.assert_called_once()
        mock.go_out_of_drawzone_task._stop.assert_called_once()

    def test_task_status_change_to_done_at_the_end_of_execution(self):
        x_robot_position = 10
        y_robot_position = 10
        robot_controler = Mock(RobotController)
        go_out_of_drawzone_task = GoOutOfDrawzoneTask(robot_controler)

        mock = Mock()
        mock.go_out_of_drawzone_task._stop()

        go_out_of_drawzone_task.execute(x_robot_position, y_robot_position)

        mock.go_out_of_drawzone_task._stop.assert_called_once()
        self.assertEquals(go_out_of_drawzone_task.status_flag, 1)

    def test_subtasks_are_executed_in_order(self):
        x_robot_position = 10
        y_robot_position = 10
        robot_controler = Mock(RobotController)
        go_out_of_drawzone_task = GoOutOfDrawzoneTask(robot_controler)

        go_out_of_drawzone_mock = MagicMock()
        with patch('robot.task.gooutofdrawzonetask.GoOutOfDrawzoneTask._quit_draw_zone', go_out_of_drawzone_mock.function1), \
                patch('robot.task.gooutofdrawzonetask.GoOutOfDrawzoneTask._stop', go_out_of_drawzone_mock.function2):

            expected = [
                call.function1(),
                call.function2()
            ]

            go_out_of_drawzone_task.execute(x_robot_position, y_robot_position)

            self.assertEqual(go_out_of_drawzone_mock.mock_calls, expected)