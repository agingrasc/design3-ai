from unittest import TestCase
from unittest.mock import Mock, MagicMock, patch, call

from mcu.robotcontroller import RobotController
from robot.task.takepicturetask import TakePictureTask


class TakePictureTaskTest(TestCase):

    def test_execute_all_the_subtasks(self):
        x_robot_position = 10
        y_robot_position = 10
        robot_controler = Mock(RobotController)
        take_picture_task = TakePictureTask(robot_controler)

        mock = Mock()
        mock.take_picture_task._take_image()
        mock.take_picture_task._analyse_picture()
        mock.take_picture_task._stop()

        take_picture_task.execute(x_robot_position, y_robot_position)

        mock.take_picture_task._take_image.assert_called_once()
        mock.take_picture_task._analyse_picture.assert_called_once()
        mock.take_picture_task._stop.assert_called_once()

    def test_task_status_change_to_done_at_the_end_of_execution(self):
        x_robot_position = 10
        y_robot_position = 10
        robot_controler = Mock(RobotController)
        take_picture_task = TakePictureTask(robot_controler)

        mock = Mock()
        mock.take_picture_task._take_image()
        mock.take_picture_task._analyse_picture()
        mock.take_picture_task._stop()

        take_picture_task.execute(x_robot_position, y_robot_position)

        mock.take_picture_task._stop.assert_called_once()
        self.assertEquals(take_picture_task.status_flag, 1)

    def test_subtasks_are_executed_in_order(self):
        x_robot_position = 10
        y_robot_position = 10
        robot_controler = Mock(RobotController)
        take_picture_task = TakePictureTask(robot_controler)

        take_picture_mock = MagicMock()
        with patch('robot.task.takepicturetask.TakePictureTask._take_image', take_picture_mock.function1), \
                patch('robot.task.takepicturetask.TakePictureTask._analyse_picture', take_picture_mock.function2), \
                patch('robot.task.takepicturetask.TakePictureTask._stop', take_picture_mock.function3):

            expected = [
                call.function1(),
                call.function2(),
                call.function3()
            ]

            take_picture_task.execute(x_robot_position, y_robot_position)

            self.assertEqual(take_picture_mock.mock_calls, expected)