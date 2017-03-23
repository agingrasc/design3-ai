import unittest
from unittest.mock import Mock, call

from mcu.robotcontroller import RobotController
from domain.robot.task.identifyantennatask.identifyantennatask import IdentifyAntennaTask
from domain.robot.task.identifyantennatask import identifyantennatask

VALID_WIDTH = 20
VALID_MAX_SIGNAL_POSITION = Mock(pos_x=10, pos_y=10)


class IdentifyAntennaTaskTest(unittest.TestCase):
    def setUp(self):
        self.drawer = Mock()
        self.antenna = Mock()
        self.feedback = Mock()
        self.vision_regulation = Mock()
        self.global_information = Mock()
        self.start_antenna_position = Mock(pos_x=5, pos_y=10)
        self.end_antenna_position = Mock(pos_x=20, pos_y=10)
        self.antenna.get_start_antenna_position.return_value = self.start_antenna_position
        self.antenna.get_end_antenna_position.return_value = self.end_antenna_position
        self.antenna.get_max_signal_position.return_value = VALID_MAX_SIGNAL_POSITION
        self.global_information.get_robot_width.return_value = VALID_WIDTH

    def test_call_go_to_position_correctly(self):
        task = IdentifyAntennaTask(self.drawer, self.antenna, self.feedback,
                                   self.vision_regulation,
                                   self.global_information)

        task.execute()

        expected_calls = [
            call(self.start_antenna_position), call(self.end_antenna_position),
            call(VALID_MAX_SIGNAL_POSITION)
        ]

        self.vision_regulation.go_to_position.assert_has_calls(expected_calls)

    def test_call_antenna_correctly(self):
        task = IdentifyAntennaTask(self.drawer, self.antenna, self.feedback,
                                   self.vision_regulation,
                                   self.global_information)

        task.execute()
        expected_calls = [
            call.get_start_antenna_position(), call.start_recording(),
            call.get_end_antenna_position(), call.end_recording(),
            call.get_max_signal_position()
        ]

        self.antenna.assert_has_calls(expected_calls)

    def test_call_drawer_correctly(self):
        max_segment_position = Mock(pos_x=3, pos_y=10)
        self.antenna.get_segment_max_signal_antenna.return_value = max_segment_position
        task = IdentifyAntennaTask(self.drawer, self.antenna, self.feedback,
                                   self.vision_regulation,
                                   self.global_information)

        task.execute()

        expected_calls = [
            call([VALID_MAX_SIGNAL_POSITION, max_segment_position])
        ]

        self.drawer.draw.assert_has_calls(expected_calls)
