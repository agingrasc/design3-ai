import unittest
from unittest.mock import Mock, call

from domain.robot.task.identifyantennataskproxy.identifyantennataskproxy import IdentifyAntennaTaskProxy


class IdentifyAntennaTaskTestProxy(unittest.TestCase):
    def setUp(self):
        self.identify_antenna_task = Mock()
        self.vision_regulation = Mock()
        self.global_information = Mock()
        self.blackboard = Mock()


    def test_call_identification_other_cycles_correctly(self):

        task = IdentifyAntennaTaskProxy(
            self.identify_antenna_task, self.blackboard, self.vision_regulation, self.global_information
        )

        self.blackboard.has_antenna_position.return_value = True

        task.execute()

        self.global_information.send_path.assert_called_once()
        self.global_information.get_robot_position.assert_called_once()
        self.vision_regulation.oriente_robot.assert_called_once()
        self.vision_regulation.go_to_position.assert_called_once()

    def test_call_identification_first_cycles_correctly(self):

        task = IdentifyAntennaTaskProxy(
            self.identify_antenna_task, self.blackboard, self.vision_regulation, self.global_information
        )

        self.blackboard.has_antenna_position.return_value = False

        task.execute()

        self.identify_antenna_task.execute.assert_called_once()
