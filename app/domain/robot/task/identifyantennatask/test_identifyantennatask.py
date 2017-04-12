import unittest
from unittest.mock import Mock, call

from domain.robot.task.identifyantennatask.identifyantennatask import IdentifyAntennaTask

VALID_WIDTH = 20
VALID_MAX_SIGNAL_POSITION = Mock(pos_x=10, pos_y=10)
VALID_PATH_START = [(35, 35), (40, 40), (45, 45)]
VALID_PATH_END = [(15, 35), (20, 40), (30, 45)]
VALID_PATH_MAX = [(10, 30), (25, 45)]


class IdentifyAntennaTaskTest(unittest.TestCase):
    def setUp(self):
        self.antenna = Mock()
        self.feedback = Mock()
        self.vision_regulation = Mock()
        self.global_information = Mock()
        self.pathfinding_application_service = Mock()
        self.start_antenna_position = Mock(pos_x=5, pos_y=10)
        self.end_antenna_position = Mock(pos_x=20, pos_y=10)
        self.max_signal_position= Mock(pos_x=25, pos_y=45)
        self.antenna.get_start_antenna_position.return_value = self.start_antenna_position
        self.antenna.get_stop_antenna_position.return_value = self.end_antenna_position
        self.antenna.get_max_signal_position.return_value = self.max_signal_position
        self.global_information.get_robot_width.return_value = VALID_WIDTH
        self.blackboard = Mock()
        self.pathfinding_application_service.find.side_effect = [VALID_PATH_START, VALID_PATH_END, VALID_PATH_MAX]
        self.global_information.get_robot_position = Mock(pos_x=10, pos_y=10)
        self.blackboard.get_mark_move.return_value = Mock(pos_x=10, pos_y=10)

    def test_call_go_to_multiple_positions_correctly(self):
        task = IdentifyAntennaTask(
            self.antenna, self.feedback, self.vision_regulation, self.global_information, self.blackboard, self.pathfinding_application_service
        )

        task.execute()

        expected_calls = [
            call(VALID_PATH_START), call(VALID_PATH_END)
        ]

        self.vision_regulation.go_to_positions.assert_has_calls(expected_calls)

    def test_call_antenna_correctly(self):
        task = IdentifyAntennaTask(
            self.antenna, self.feedback, self.vision_regulation, self.global_information, self.blackboard, self.pathfinding_application_service
        )

        task.execute()

        expected_calls = [
            call.get_start_antenna_position(), call.start_recording(), call.get_stop_antenna_position(),
            call.end_recording(), call.get_max_signal_position()
        ]

        self.antenna.assert_has_calls(expected_calls)

    def test_call_pathfinder_correctly(self):
        task = IdentifyAntennaTask(
            self.antenna, self.feedback, self.vision_regulation, self.global_information, self.blackboard,
            self.pathfinding_application_service
        )

        task.execute()

        expected_calls = [
            call(self.global_information, self.start_antenna_position),
            call(self.global_information, self.end_antenna_position), call(self.global_information, self.max_signal_position)
        ]

        self.pathfinding_application_service.find.assert_has_calls(expected_calls)
