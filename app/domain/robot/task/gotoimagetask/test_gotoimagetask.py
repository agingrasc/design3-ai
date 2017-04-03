from unittest import TestCase
from unittest.mock import Mock, call

from domain.robot.task.gotoimagetask.gotoimagetask import GoToImageTask
from domain.robot.task.gotoimagetask.gotoimagetask import images_position

VALID_OBSTACLES_LIST = [Mock(pos_x=50, pos_y=50, radius=2, Tag=""), Mock(pos_x=40, pos_y=40, radius=2, Tag="")]
WIDTH_TABLE = 1120
LENGTH_TABLE = 2300
VALID_PATH = [(35, 35), (40, 40), (45, 45)]
VALID_IMAGE_ID = 2


class GoToImageTaskTest(TestCase):
    def setUp(self):
        self.feedback = Mock()
        self.vision_regulation = Mock()
        self.global_information = Mock()
        self.pathfinding_application_service = Mock()
        self.blackboard = Mock()
        self.robot_position = Mock(pos_x=30, pos_y=30)
        self.global_information.get_obstacles.return_value = VALID_OBSTACLES_LIST
        self.global_information.get_robot_position.return_value = self.robot_position
        self.global_information.get_gameboard_width.return_value = WIDTH_TABLE
        self.global_information.get_gameboard_length.return_value = LENGTH_TABLE
        self.blackboard.get_image_id.return_value = VALID_IMAGE_ID
        self.pathfinding_application_service.find.return_value = VALID_PATH

    def test_get_information_of_the_gameboard_correctly(self):
        task = GoToImageTask(
            self.feedback, self.vision_regulation, self.global_information, self.pathfinding_application_service,
            self.blackboard
        )

        task.execute()

        expected_calls = [
            call.get_obstacles(), call.get_robot_position(), call.get_gameboard_width(), call.get_gameboard_length()
        ]

        self.pathfinding_application_service.find.assert_called_once_with(
            self.global_information, images_position[VALID_IMAGE_ID]
        )

    def test_set_destination_to_robot(self):
        task = GoToImageTask(
            self.feedback, self.vision_regulation, self.global_information, self.pathfinding_application_service,
            self.blackboard
        )

        task.execute()

        self.pathfinding_application_service.find.assert_called_once()
