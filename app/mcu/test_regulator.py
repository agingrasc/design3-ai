import unittest

from domain.gameboard.position import Position
from mcu.regulator import PIPositionRegulator

TEST_DELTA_T = 0.1


class TestRegulator(unittest.TestCase):

    def setUp(self):
        self.regulator = PIPositionRegulator(1, 1, 0, 0, 0, 5, 100, 20, 20, 0, 0)
        self.regulator.setpoint = Position(1000, 1000, 0)

    def test_no_move(self):
        null_actual_position = Position(1000, 1000, 0)
        speeds = self.regulator.next_speed_command(null_actual_position, delta_t=TEST_DELTA_T)
        expected_speeds = [0, 0, 0]
        self.assertEqual(expected_speeds, speeds)

    def test_far_negative_move(self):
        self.regulator.setpoint = Position(0, 0, 0)
        far_actual_position = Position(1000, 1000, 0)
        speeds = self.regulator.next_speed_command(far_actual_position, delta_t=TEST_DELTA_T)
        expected_speeds = [-70, -70, 0]
        self.assertEqual(expected_speeds, speeds)

    def test_far_positive_move(self):
        origin_actual_position = Position(0, 0, 0)
        speeds = self.regulator.next_speed_command(origin_actual_position, delta_t=TEST_DELTA_T)
        expected_speeds = [70, 70, 0]
        self.assertEqual(expected_speeds, speeds)

    def test_integral_action(self):
        close_actual_position = Position(1000-50, 1000-50, 0)
        first_iteration_speeds = self.regulator.next_speed_command(close_actual_position, delta_t=TEST_DELTA_T)
        first_iteration_expected_speeds = [55, 55, 0]
        self.assertEqual(first_iteration_expected_speeds, first_iteration_speeds)

        second_iteration_speeds = self.regulator.next_speed_command(close_actual_position, delta_t=TEST_DELTA_T)
        second_iteration_expected_speeds = [58, 58, 0]
        self.assertEqual(second_iteration_expected_speeds, second_iteration_speeds)

    def test_positive_saturate_accumulator(self):
        origin_actual_position = Position(0, 0, 0)
        self.regulator.next_speed_command(origin_actual_position, delta_t=TEST_DELTA_T)
        self.regulator.next_speed_command(origin_actual_position, delta_t=TEST_DELTA_T)
        maxed_accumulator = [100, 100, 0]
        self.assertEqual(maxed_accumulator, self.regulator.accumulator)

    def test_negative_saturate_accumulator(self):
        origin_setpoint = Position(0, 0, 0)
        self.regulator.setpoint = origin_setpoint
        far_actual_position = Position(1000, 1000, 0)
        self.regulator.next_speed_command(far_actual_position, delta_t=TEST_DELTA_T)
        self.regulator.next_speed_command(far_actual_position, delta_t=TEST_DELTA_T)
        maxed_accumulator = [-100, -100, 0]
        self.assertEqual(maxed_accumulator, self.regulator.accumulator)

    def test_relinearize(self):
        very_close_actual_position = Position(1000-10, 1000-10, 0)
        speeds = self.regulator.next_speed_command(very_close_actual_position, delta_t=TEST_DELTA_T)
        expected_speeds = [31, 31, 0]
        self.assertEqual(expected_speeds, speeds)

    def test_is_arrived_far(self):
        origin_actual_position = Position(0, 0, 0)
        is_arrived = self.regulator.is_arrived(origin_actual_position)
        expected_is_arrived = False
        self.assertEqual(expected_is_arrived, is_arrived)

    def test_is_arrived_close(self):
        close_actual_position = Position(1000-10, 1000-10, 0)
        is_arrived = self.regulator.is_arrived(close_actual_position, 10)
        expected_is_arrived = True
        self.assertEqual(expected_is_arrived, is_arrived)

    def test_set_speed(self):
        initial_speed = self.regulator.constants.max_cmd
        self.regulator.set_speed(20, 10)
        updated_speed = self.regulator.constants.max_cmd
        self.assertNotEqual(initial_speed, updated_speed)
