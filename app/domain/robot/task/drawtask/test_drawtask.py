import unittest
from unittest.mock import Mock, MagicMock, patch, call

from domain.robot.task.drawtask import drawtask

VALID_MESSAGE = drawtask.MESSAGE


class DrawTaskTest(unittest.TestCase):
    def setUp(self):
        self.feedback = Mock()
        self.drawer = Mock()
        self.blackboard = Mock()

    def test_called_all_subtask(self):
        task = drawtask.DrawTask(self.feedback, self.drawer, self.blackboard)
        task.execute()

        self.feedback.send_comment.assert_called_once()
        self.blackboard.get_segments_image.assert_called_once()
        self.drawer.draw.assert_called_once()

    def test_called_drawer_with_good_input(self):
        task = drawtask.DrawTask(self.feedback, self.drawer, self.blackboard)
        return_value_interpreter = ["position1", "position2"]
        self.blackboard.get_image_segments.return_value = return_value_interpreter
        task.execute()

        self.drawer.draw.assert_called_with(return_value_interpreter)
