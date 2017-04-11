import unittest
import math
from domain.gameboard import position


class PositionTest(unittest.TestCase):
    def setUp(self):
        self.a_valid_x = 5
        self.a_valid_y = 27
        self.a_valid_angle = math.pi

    def test_samexy_init(self):
        pos = position.Position(self.a_valid_x, self.a_valid_x)

        angle = -1 * math.atan(1.0)
        distance = math.sqrt(float(self.a_valid_x**2) + float(self.a_valid_x**2))
        self.assertEqual(distance, pos.get_norm())
        self.assertEqual(angle, pos.get_angle())

    def test_differentxy_init(self):
        pos = position.Position(self.a_valid_x, self.a_valid_y)

        angle = -1 * math.atan(self.a_valid_y / self.a_valid_x)
        distance = math.sqrt(float(self.a_valid_x**2) + float(self.a_valid_y**2))
        self.assertEqual(distance, pos.get_norm())
        self.assertEqual(angle, pos.get_angle())

    def test_samexy_setcartesian(self):
        pos = position.Position(self.a_valid_x, self.a_valid_x)

        pos.pos_y = self.a_valid_y

        angle = -1 * math.atan(self.a_valid_y / self.a_valid_x)
        distance = math.sqrt(float(self.a_valid_x**2) + float(self.a_valid_y**2))
        self.assertEqual(distance, pos.get_norm())
        self.assertEqual(angle, pos.get_angle())

    def test_differentxy_setcartesian(self):
        pos = position.Position(self.a_valid_x, self.a_valid_y)

        pos.pos_y = self.a_valid_x

        angle = -1 * math.atan(1.0)
        distance = math.sqrt(float(self.a_valid_x**2) + float(self.a_valid_x**2))
        self.assertEqual(distance, pos.get_norm())
        self.assertEqual(angle, pos.get_angle())

    def test_renormalize_smaller(self):
        pos = position.Position(100, 100)
        result = pos.renormalize(10)
        expected = position.Position(7, 7)
        self.assertEqual(expected, result)

    def test_renormalize_larger(self):
        pos = position.Position(100, 100)
        result = pos.renormalize(200)
        expected = position.Position(141, 141)
        self.assertEqual(expected, result)

    def test_multiply(self):
        pos = position.Position(100, 100)
        result = pos.multiply(1.5)
        expected = position.Position(150, 150)
        self.assertEqual(expected, result)
