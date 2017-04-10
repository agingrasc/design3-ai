import unittest
from unittest.mock import Mock, call

from domain.robot.task.identifyantennataskproxy.identifyantennataskproxy import IdentifyAntennaTaskProxy

VALID_PATH_MAX = [(10, 30), (25, 45)]
VALID_MAX_SIGNAL_POSITION = Mock(pos_x=10, pos_y=10)


class IdentifyAntennaTaskTestProxy(unittest.TestCase):
    def setUp(self):
        self.identify_antenna_task = Mock()
        self.vision_regulation = Mock()
        self.global_information = Mock()
        self.blackboard = Mock()
        self.pathfinding_application_service = Mock()
        self.pathfinding_application_service.find.return_value = VALID_PATH_MAX


    def test_call_identification_other_cycles_correctly(self):

        task = IdentifyAntennaTaskProxy(
            self.identify_antenna_task, self.blackboard, self.vision_regulation,
            self.global_information, self.pathfinding_application_service
        )

        self.blackboard.has_antenna_position.return_value = True

        task.execute()

        self.blackboard.get_antenna_position.assert_called_once()
        self.vision_regulation.go_to_positions.assert_called_once()

    def test_call_pathfinder_correctly(self):
        task = IdentifyAntennaTaskProxy(
            self.identify_antenna_task, self.blackboard, self.vision_regulation,
            self.global_information, self.pathfinding_application_service
        )

        self.blackboard.has_antenna_position.return_value = True
        self.blackboard.get_antenna_position.return_value = VALID_MAX_SIGNAL_POSITION

        task.execute()

        expected_calls = [
            call(self.global_information, VALID_MAX_SIGNAL_POSITION),
        ]

        self.pathfinding_application_service.find.assert_has_calls(expected_calls)

    def test_call_identification_first_cycles_correctly(self):

        task = IdentifyAntennaTaskProxy(
            self.identify_antenna_task, self.blackboard, self.vision_regulation,
            self.global_information, self.pathfinding_application_service
        )

        self.blackboard.has_antenna_position.return_value = False

        task.execute()

        self.identify_antenna_task.execute.assert_called_once()
