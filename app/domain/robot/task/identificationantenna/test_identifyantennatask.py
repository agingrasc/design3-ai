import unittest
from unittest.mock import Mock, call

from mcu.robotcontroller import RobotController
from domain.robot.task.identificationantenna.identifyantennatask import IdentifyAntennaTask
from domain.robot.task.identificationantenna import identifyantennatask

VALID_WIDTH = 20
VALID_MAX_SIGNAL_POSITION = Mock(
    pos_x=identifyantennatask.X_START_OFFSET + 10,
    pos_y=identifyantennatask.Y_OFFSET)


class IdentifyAntennaTaskTest(unittest.TestCase):
    def setUp(self):
        self.drawer = Mock()
        self.antenna = Mock()
        self.feedback = Mock()
        self.vision_regulation = Mock()
        self.global_information = Mock()
        self.star_antenna_position = Mock(
            pos_x=identifyantennatask.X_START_OFFSET + (VALID_WIDTH / 2) + 1,
            pos_y=identifyantennatask.Y_OFFSET + (VALID_WIDTH / 2) + 1)
        self.end_antenna_position = Mock(
            pos_x=identifyantennatask.X_END_OFFSET + (VALID_WIDTH / 2) + 1,
            pos_y=identifyantennatask.Y_OFFSET + (VALID_WIDTH / 2) + 1)

    def test_given_valid_start_antenna_position_when_execte_robot_go_there(
            self):
        self.antenna.get_start_antenna_position.return_value = self.star_antenna_position
        self.antenna.get_end_antenna_position.return_value = self.end_antenna_position

        self.global_information.get_robot_width.return_value = VALID_WIDTH
        task = IdentifyAntennaTask(self.drawer, self.antenna, self.feedback,
                                   self.vision_regulation,
                                   self.global_information)

        task.execute()

        expected_calls = [
            call(
                self.vision_regulation.go_to_position(
                    self.star_antenna_position)), call(
                        self.vision_regulation.go_to_position(
                            self.end_antenna_position)), call(
                                self.vision_regulation.go_to_position(
                                    VALID_MAX_SIGNAL_POSITION))
        ]

        self.vision_regulation.assert_has_calls(expected_calls)
