from unittest import TestCase
from unittest.mock import Mock, call

from domain.robot.task.gotoimagetask.gotoimagetask import GoToImageTask

VALID_OBSTACLES_LIST = [
    Mock(pos_x=50, pos_y=50, radius=2, Tag=""), Mock(
        pos_x=40, pos_y=40, radius=2, Tag="")
]
WIDTH_TABLE = 1120
LENGTH_TABLE = 2300
VALID_PATH = [(35, 35), (40, 40), (45, 45)]
VALID_DESTINATIONS_PATH = [(40, 40), (45, 45)]
VALID_IMAGE_POSITION = Mock(pos_x=200, pos_y=10)


class GoToImageTaskTest(TestCase):
    def setUp(self):
        self.feedback = Mock()
        self.vision_regulation = Mock()
        self.global_information = Mock()
        self.image_position_finder = Mock()
        self.pathfinding_application_service = Mock()
        self.get_segments = Mock()
        self.robot_position = Mock(pos_x=30, pos_y=30)
        self.global_information.get_obstacles.return_value = VALID_OBSTACLES_LIST
        self.global_information.get_robot_position.return_value = self.robot_position
        self.global_information.get_gameboard_width.return_value = WIDTH_TABLE
        self.global_information.get_gameboard_length.return_value = LENGTH_TABLE
        self.image_position_finder.getImagePosition.return_value = VALID_IMAGE_POSITION
        self.pathfinding_application_service.find.return_value = VALID_PATH
        self.get_segments.get_filter_path.return_value = VALID_DESTINATIONS_PATH

    def test_get_information_of_the_gameboard_correctly(self):
        task = GoToImageTask(self.feedback, self.vision_regulation,
                             self.global_information,
                             self.pathfinding_application_service,
                             self.get_segments, self.image_position_finder)

        task.execute()

        expected_calls = [
            call.get_obstacles(), call.get_robot_position(),
            call.get_gameboard_width(), call.get_gameboard_length()
        ]

        self.global_information.assert_has_calls(expected_calls)

    def test_set_destination_to_robot(self):
        task = GoToImageTask(self.feedback, self.vision_regulation,
                             self.global_information,
                             self.pathfinding_application_service,
                             self.get_segments, self.image_position_finder)

        task.execute()

        self.pathfinding_application_service.find.assert_called_once()
