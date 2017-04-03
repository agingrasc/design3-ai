import numpy as np
from unittest import TestCase
from unittest.mock import Mock, call

from mcu.robotcontroller import RobotController
from domain.robot.task.initialorientationtask.initialorientationtask import InitialOrientationTask

INITIAL_ANGLE = 0.79


class InitialOrientationTaskTest(TestCase):
    def setUp(self):
        self.feedback = Mock()
        self.vision_regulation = Mock()
        self.global_information = Mock()

    def test_set_orientation(self):
        task = InitialOrientationTask(self.feedback, self.vision_regulation, self.global_information)

        task.execute()

        rebot_orientation = 1
        self.global_information.get_robot_orientation.return_value = rebot_orientation
        self.vision_regulation.oriente_robot.assert_called_once_with(np.deg2rad(INITIAL_ANGLE))

    def test_send_feedback(self):
        task = InitialOrientationTask(self.feedback, self.vision_regulation, self.global_information)
        task.execute()
        self.feedback.send_comment.assert_called_once()
