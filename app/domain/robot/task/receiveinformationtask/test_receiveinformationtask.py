import unittest
from unittest.mock import Mock, call

from mcu.robotcontroller import RobotController
from domain.robot.task.receiveinformationtask.receiveinformationtask import ReceiveInformationTask

VALID_MAX_SIGNAL_POSITION = Mock(pos_x=10, pos_y=10)
VALID_IMAGE_NUMBER = 2
VALID_IMAGE_ORIENTATION = "NORD"
VALID_IMAGE_MAGNIFICATION = 4


class ReceiveInformationsTaskTest(unittest.TestCase):
    def setUp(self):
        self.decoder = Mock()
        self.feedback = Mock()
        self.vision_regulation = Mock()
        self.blackboard = Mock()
        self.global_information = Mock()
        self.decoder.get_image_number.return_value = VALID_IMAGE_NUMBER
        self.decoder.get_image_orientation.return_value = VALID_IMAGE_ORIENTATION
        self.decoder.get_image_magnification.return_value = VALID_IMAGE_MAGNIFICATION

    def test_call_get_informations_correctly(self):
        task = ReceiveInformationTask(self.feedback, self.decoder, self.vision_regulation, self.blackboard)

        task.execute()

        expected_calls = [
            call.decode_information(), call.get_image_number(), call.get_image_orientation(),
            call.get_image_magnification()
        ]

        self.decoder.assert_has_calls(expected_calls)

    def test_called_all_subtask(self):
        task = ReceiveInformationTask(self.feedback, self.decoder, self.vision_regulation, self.blackboard)
        task.execute()

        self.feedback.send_comment.assert_called_once()
        self.decoder.decode_information.assert_called_once()
        self.decoder.get_image_number.assert_called_once()
        self.decoder.get_image_orientation.assert_called_once()
        self.decoder.get_image_magnification.assert_called_once()
