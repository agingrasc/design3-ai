from unittest import TestCase
from unittest.mock import Mock

from api.gotoposition.positionassembler import PositionAssembler

VALID_JSON_THETA = "2.05"

VALID_JSON_X_POSITION = "50.34"
VALID_JSON_Y_POSITION = "100.24"
VALID_X_POSITION_NO_SCALING = 50
VALID_Y_POSITION_NO_SCALING = 100

VALID_THETA = 2.05

SCALING = 10

VALID_X_POSITION_SCALING = 5
VALID_Y_POSITION_SCALING = 10

DEFAULT_THETA = 0


class PositionAssemblerTest(TestCase):
    def test_given_valid_json_position_without_scaling_when_convert_position_from_dto_then_return_position(
            self):
        valid_json_position = self.get_json_position(
            VALID_JSON_X_POSITION, VALID_JSON_Y_POSITION, VALID_THETA)
        self.position_assembler = PositionAssembler()

        valid_position = self.position_assembler.convert_position_from_json(
            valid_json_position)

        self.assertEqual(VALID_X_POSITION_NO_SCALING, valid_position.pos_x)
        self.assertEqual(VALID_Y_POSITION_NO_SCALING, valid_position.pos_y)
        self.assertEqual(VALID_THETA, valid_position.theta)

    def test_given_valid_json_position_with_scaling_when_convert_position_from_dto_then_return_position(
            self):
        valid_json_position = self.get_json_position(
            VALID_JSON_X_POSITION, VALID_JSON_Y_POSITION, VALID_THETA)
        self.position_assembler = PositionAssembler(SCALING)

        valid_position = self.position_assembler.convert_position_from_json(
            valid_json_position)

        self.assertEqual(VALID_X_POSITION_SCALING, valid_position.pos_x)
        self.assertEqual(VALID_Y_POSITION_SCALING, valid_position.pos_y)
        self.assertEqual(VALID_THETA, valid_position.theta)

    def test_given_no_theta_when_convert_position_from_dto_then_defaul_theta_value(
            self):
        valid_json_position = {
            'x': VALID_X_POSITION_NO_SCALING,
            'y': VALID_Y_POSITION_NO_SCALING
        }
        self.position_assembler = PositionAssembler(SCALING)

        valid_position = self.position_assembler.convert_position_from_json(
            valid_json_position)

        self.assertEqual(DEFAULT_THETA, valid_position.theta)

    def get_json_position(self, position_x, position_y, theta):
        position = {'x': position_x, 'y': position_y, 'theta': theta}
        return position
