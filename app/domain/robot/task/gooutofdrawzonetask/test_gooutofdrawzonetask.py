from unittest import TestCase
from unittest.mock import Mock, call

from domain.robot.task.gooutofdrawzonetask.gooutofdrawzonetask import GoOutOfDrawzoneTask

VALID_OBSTACLES_LIST = [Mock(pos_x=50, pos_y=50, radius=2, Tag=""), Mock(pos_x=40, pos_y=40, radius=2, Tag="")]
VALID_SAFEZONE_POSITION = Mock(pos_x=45, pos_y=45)
WIDTH_TABLE = 1120
LENGTH_TABLE = 2300
VALID_PATH = [(35, 35), (40, 40), (45, 45)]
VALID_DESTINATIONS_PATH = [(40, 40), (45, 45)]


class GoOutOfDrawzoneTaskTest(TestCase):
    def setUp(self):
        self.feedback = Mock()
        self.vision_regulation = Mock()
        self.global_information = Mock()
        self.destination_calculator = Mock()
        self.pathfinding_application_service = Mock()
        self.get_segments = Mock()
        self.robot_position = Mock(pos_x=30, pos_y=30)
        self.global_information.get_obstacles.return_value = VALID_OBSTACLES_LIST
        self.global_information.get_robot_position.return_value = self.robot_position
        self.global_information.get_gameboard_width.return_value = WIDTH_TABLE
        self.global_information.get_gameboard_length.return_value = LENGTH_TABLE
        self.destination_calculator.get_safezone.return_value = VALID_SAFEZONE_POSITION
        self.pathfinding_application_service.find.return_value = VALID_PATH
        self.get_segments.get_filter_path.return_value = VALID_DESTINATIONS_PATH

    """
    def test_get_information_of_the_gameboard_correctly(self):
        task = GoOutOfDrawzoneTask(
            self.feedback, self.vision_regulation, self.destination_calculator, self.global_information
        )

        task.execute()

        expected_calls = [
            call.get_obstacles(), call.get_robot_position(), call.get_gameboard_width(), call.get_gameboard_length()
        ]

        self.global_information.assert_has_calls(expected_calls)

    def test_get_safezone_correctly(self):
        task = GoOutOfDrawzoneTask(
            self.feedback, self.vision_regulation, self.destination_calculator, self.global_information
        )

        task.execute()

        expected_calls = [call(VALID_OBSTACLES_LIST, self.robot_position)]

        self.destination_calculator.get_safezone.assert_has_calls(expected_calls)

    def test_call_go_to_position_correctly(self):
        task = GoOutOfDrawzoneTask(
            self.feedback, self.vision_regulation, self.destination_calculator, self.global_information,
            self.pathfinding_application_service, self.get_segments
        )

        task.execute()

        expected_calls = [call(VALID_DESTINATIONS_PATH[0]), call(VALID_DESTINATIONS_PATH[1])]

        self.vision_regulation.go_to_position.assert_has_calls(expected_calls)

    def test_get_path_to_safezone_correctly(self):
        task = GoOutOfDrawzoneTask(
            self.feedback, self.vision_regulation, self.destination_calculator, self.global_information,
            self.pathfinding_application_service, self.get_segments
        )

        task.execute()

        expected_calls = [
            call(VALID_OBSTACLES_LIST, WIDTH_TABLE, LENGTH_TABLE, self.robot_position, VALID_SAFEZONE_POSITION)
        ]

        self.pathfinding_application_service.find.assert_has_calls(expected_calls)

    def test_get_path_corners_correctly(self):
        task = GoOutOfDrawzoneTask(
            self.feedback, self.vision_regulation, self.destination_calculator, self.global_information,
            self.pathfinding_application_service, self.get_segments
        )

        task.execute()

        expected_calls = [call(VALID_PATH)]

        self.get_segments.get_filter_path.assert_has_calls(expected_calls)

    def test_called_all_subtask(self):
        task = GoOutOfDrawzoneTask(
            self.feedback, self.vision_regulation, self.destination_calculator, self.global_information,
            self.pathfinding_application_service, self.get_segments
        )
        task.execute()

        self.feedback.send_comment.assert_called_once()
        self.destination_calculator.get_safezone.assert_called_once()
        self.global_information.get_obstacles.assert_called_once()
        self.global_information.get_robot_position.assert_called_once()
        self.pathfinding_application_service.find.assert_called_once()
       self.get_segments.get_filter_path.assert_called_once()
       """
