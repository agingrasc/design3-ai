from unittest import TestCase
from unittest.mock import Mock

from api.gotoposition.dimensionassembler import DimensionAssembler

VALID_JSON_X_DIMENSION_NO_SCALING = "5000.34"
VALID_JSON_Y_DIMENSION_NO_SCALING = "1000.74"
VALID_X_DIMENSION_NO_SCALING = 5000
VALID_Y_DIMENSION_NO_SCALING = 1000

SCALING = 10

VALID_X_DIMENSION_SCALING = 500
VALID_Y_DIMENSION_SCALING = 100


class ObstacleAssemblerTest(TestCase):
    def test_given_valid_json_dimension_without_scaling_when_convert_position_from_dto_then_return_dimension(self):
        valid_json_dimension = self.get_json_dimension(
            VALID_JSON_X_DIMENSION_NO_SCALING, VALID_JSON_Y_DIMENSION_NO_SCALING
        )
        self.dimension_assembler = DimensionAssembler()

        valid_dimension = self.dimension_assembler.convert_dimension_from_json(valid_json_dimension)

        self.assertEqual(VALID_X_DIMENSION_NO_SCALING, valid_dimension[0])
        self.assertEqual(VALID_Y_DIMENSION_NO_SCALING, valid_dimension[1])

    def test_given_valid_json_dimension_with_scaling_when_convert_position_from_dto_then_return_dimension(self):
        valid_json_dimension = self.get_json_dimension(
            VALID_JSON_X_DIMENSION_NO_SCALING, VALID_JSON_Y_DIMENSION_NO_SCALING
        )
        self.dimension_assembler = DimensionAssembler(SCALING)

        valid_dimension = self.dimension_assembler.convert_dimension_from_json(valid_json_dimension)

        self.assertEqual(VALID_X_DIMENSION_SCALING, valid_dimension[0])
        self.assertEqual(VALID_Y_DIMENSION_SCALING, valid_dimension[1])

    def get_json_position(self, position_x, position_y, theta):
        position = {'x': position_x, 'y': position_y, 'theta': theta}
        return position

    def get_json_dimension(self, width, lenght):
        dimension = {'width': width, 'length': lenght}
        return dimension
