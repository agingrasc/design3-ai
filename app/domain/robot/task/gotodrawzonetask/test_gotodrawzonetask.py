from unittest import TestCase
from unittest.mock import Mock, call

from mcu.robotcontroller import RobotController
from domain.robot.task.gotodrawzonetask.gotodrawzonetask import GoToDrawzoneTask

VALID_PATH = [Mock(pos_x=10, pos_y=10, theta=0), Mock(pos_x=15, pos_y=15, theta=0)]

class GoToDrawzoneTaskTest(TestCase):
    def setUp(self):
        self.feedback = Mock()
        self.vision_regulation = Mock()
        self.global_information = Mock()
        self.pathfinder_service = Mock()
        self.blackboard = Mock()
        self.go_to_draw_zone_task = GoToDrawzoneTask(
            self.feedback, self.vision_regulation, self.global_information, self.pathfinder_service, self.blackboard
        )

    def test_execute_correct_data(self):
        points = [Mock()]
        self.blackboard.get_image_segments.return_value = points

        positions = [Mock(), Mock(), Mock()]
        self.pathfinder_service.find.return_value = positions

        path = []
        for position in positions:
            path.append(position)
        path.pop(len(path) - 1)
        expected_calls = [
            call(path)
        ]

        self.go_to_draw_zone_task.execute()

        self.blackboard.get_image_segments.assert_called_once()
        self.pathfinder_service.find.assert_called_once_with(self.global_information, points[0])
        self.vision_regulation.go_to_positions.assert_has_calls(expected_calls)

    def test_send_comment(self):
        self.blackboard.get_image_segments.return_value = [Mock()]
        self.pathfinder_service.find.return_value = VALID_PATH

        self.go_to_draw_zone_task.execute()

        self.feedback.send_comment.assert_called_once()
