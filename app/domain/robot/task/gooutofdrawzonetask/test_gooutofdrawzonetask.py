from unittest import TestCase
from unittest.mock import Mock, call

from domain.robot.task.gooutofdrawzonetask.gooutofdrawzonetask import GoOutOfDrawzoneTask

VALID_OBSTACLES_LIST = [Mock(pos_x=50, pos_y=50, radius=2, Tag=""), Mock(pos_x=40, pos_y=40, radius=2, Tag="")]
VALID_SAFEZONE_POSITION = Mock(pos_x=45, pos_y=45)
WIDTH_TABLE = 1120
LENGTH_TABLE = 2300
VALID_PATH = [Mock(pos_x=35, pos_y=35, theta=0), Mock(pos_x=40, pos_y=40, theta=0), Mock(pos_x=45, pos_y=45, theta=0)]
VALID_DESTINATIONS_PATH = [(40, 40), (45, 45)]


class GoOutOfDrawzoneTaskTest(TestCase):
    def setUp(self):
        self.feedback = Mock()
        self.vision_regulation = Mock()
        self.global_information = Mock()
        self.destination_calculator = Mock()
        self.safe_zone_finder = Mock()
        self.safe_zone_finder.find_safe_zone.return_value = VALID_DESTINATIONS_PATH

    def test_call_go_to_position_correctly(self):
        task = GoOutOfDrawzoneTask(
            self.feedback, self.vision_regulation, self.global_information, self.safe_zone_finder
        )

        task.execute()

        self.vision_regulation.go_to_positions.a(VALID_DESTINATIONS_PATH)

    def test_call_all_submodules_once(self):
        task = GoOutOfDrawzoneTask(
            self.feedback, self.vision_regulation, self.global_information, self.safe_zone_finder
        )

        task.execute()

        self.safe_zone_finder.find_safe_zone.assert_called_once()
        self.feedback.send_comment.assert_called_once()
