from unittest import TestCase
from unittest.mock import Mock

from api.gotoposition.gotopositionAssembler import GoToPositionAssembler

VALID_JSON_X_POSITION = "50.34"
VALID_JSON_Y_POSITION = "100.24"
VALID_X_POSITION_NO_SCALING = 50
VALID_Y_POSITION_NO_SCALING = 100

VALID_JSON_X_DIMENSION_NO_SCALING = "5000.34"
VALID_JSON_Y_DIMENSION_NO_SCALING = "1000.74"
VALID_X_DIMENSION_NO_SCALING = 5000
VALID_Y_DIMENSION_NO_SCALING = 1000

SCALING = 10

VALID_X_POSITION_SCALING = 5
VALID_Y_POSITION_SCALING = 10

VALID_X_DIMENSION_SCALING = 500
VALID_Y_DIMENSION_SCALING = 100


class GoToPositionAssemblerTest(TestCase):
    def setUp(self):
        pass

    def test_given_valid_json_position_without_scaling_when_convert_position_from_dto_then_return_position(
            self):
        valid_json_position = self.get_json_position(VALID_JSON_X_POSITION,
                                                     VALID_JSON_Y_POSITION)
        self.go_to_position_assembler = GoToPositionAssembler()

        valid_position = self.go_to_position_assembler.convert_position_from_json(
            valid_json_position)

        self.assertEquals(VALID_X_POSITION_NO_SCALING, valid_position.pos_x)
        self.assertEquals(VALID_Y_POSITION_NO_SCALING, valid_position.pos_y)

    def test_given_valid_json_position_with_scaling_when_convert_position_from_dto_then_return_position(
            self):
        valid_json_position = self.get_json_position(VALID_JSON_X_POSITION,
                                                     VALID_JSON_Y_POSITION)
        self.go_to_position_assembler = GoToPositionAssembler(SCALING)

        valid_position = self.go_to_position_assembler.convert_position_from_json(
            valid_json_position)

        self.assertEquals(VALID_X_POSITION_SCALING, valid_position.pos_x)
        self.assertEquals(VALID_Y_POSITION_SCALING, valid_position.pos_y)

    def test_given_valid_json_dimension_without_scaling_when_convert_position_from_dto_then_return_dimension(
            self):
        valid_json_dimension = self.get_json_dimension(
            VALID_JSON_X_DIMENSION_NO_SCALING,
            VALID_JSON_Y_DIMENSION_NO_SCALING)
        self.go_to_position_assembler = GoToPositionAssembler()

        valid_dimension = self.go_to_position_assembler.convert_dimension_from_json(
            valid_json_dimension)

        self.assertEquals(VALID_X_DIMENSION_NO_SCALING, valid_dimension[0])
        self.assertEquals(VALID_Y_DIMENSION_NO_SCALING, valid_dimension[1])

    def test_given_valid_json_dimension_with_scaling_when_convert_position_from_dto_then_return_dimension(
            self):
        valid_json_dimension = self.get_json_dimension(
            VALID_JSON_X_DIMENSION_NO_SCALING,
            VALID_JSON_Y_DIMENSION_NO_SCALING)
        self.go_to_position_assembler = GoToPositionAssembler(SCALING)

        valid_dimension = self.go_to_position_assembler.convert_dimension_from_json(
            valid_json_dimension)

        self.assertEquals(VALID_X_DIMENSION_SCALING, valid_dimension[0])
        self.assertEquals(VALID_Y_DIMENSION_SCALING, valid_dimension[1])

    def get_json_position(self, position_x, position_y):
        position = {'x': position_x, 'y': position_y}
        return position

    def get_json_dimension(self, width, lenght):
        dimension = {'width': width, 'lenght': lenght}
        return dimension
