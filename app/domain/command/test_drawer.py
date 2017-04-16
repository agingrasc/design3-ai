import unittest
from domain.command import drawer

import numpy as np


class DrawerTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_initial_angle_is_nearest(self):
        angle = np.deg2rad(45)
        robot_angle = np.deg2rad(30)
        nearest_angle = drawer._get_nearest_angle(angle, robot_angle)
        self.assertAlmostEqual(angle, nearest_angle)
        self.assertNotAlmostEqual(np.deg2rad(135), nearest_angle)

        angle = np.deg2rad(80)
        robot_angle = np.deg2rad(70)
        nearest_angle = drawer._get_nearest_angle(angle, robot_angle)
        self.assertAlmostEqual(angle, nearest_angle)

    def test_robot_is_in_next_quarter(self):
        angle = np.deg2rad(45)
        robot_angle = np.deg2rad(120)
        nearest_angle = drawer._get_nearest_angle(angle, robot_angle)
        expected_angle = np.deg2rad(135)
        self.assertAlmostEqual(expected_angle, nearest_angle)
        self.assertNotAlmostEqual(angle, nearest_angle)

    def test_robot_is_in_previous_quarter(self):
        angle = np.deg2rad(30)
        robot_angle = np.deg2rad(-30)
        nearest_angle = drawer._get_nearest_angle(angle, robot_angle)
        expected_angle = np.deg2rad(-60)
        self.assertAlmostEqual(expected_angle, nearest_angle)
        self.assertNotAlmostEqual(angle, nearest_angle)