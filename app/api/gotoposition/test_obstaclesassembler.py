from unittest import TestCase
from api.gotoposition.obstaclesassembler import ObstacleAssembler
from unittest.mock import Mock, call

FIRST_RADIUS = 3
SECOND_RADIUS = 4

LEFT = "LEFT"
RIGHT = "RIGHT"

VALID_OBSTACLE_JSON = {
    'position': {
        'x': '56.40',
        'y': '80.3'
    },
    'dimension': {
        'width': '7',
        'lenght': '7'
    },
    'tag': LEFT
}

VALID_OBSTACLE2_JSON = {
    'position': {
        'x': '86.40',
        'y': '80.3'
    },
    'dimension': {
        'width': '9',
        'lenght': '9'
    },
    'tag': RIGHT
}


class ObstacleAssemblerTest(TestCase):
    def setUp(self):
        self.position_assembler = Mock()
        self.dimension_assembler = Mock()

    def test_given_no_obstacles_when_convert_from_json_then_return_empty_list(
            self):
        obstacle_assembler = ObstacleAssembler(self.position_assembler,
                                               self.dimension_assembler)
        obstacles = obstacle_assembler.convert_obstacles_from_json([])
        self.assertEqual([], obstacles)

    def test_given_one_obstacle_scaling_when_convert_from_json_then_called_position_and_dimension(
            self):
        self.position_assembler.convert_position_from_json.return_value = Mock(
            pos_x=56, pos_y=80)
        self.dimension_assembler.convert_dimension_from_json.return_value = (7,
                                                                             7)
        obstacle_assembler = ObstacleAssembler(self.position_assembler,
                                               self.dimension_assembler)

        obstacles = obstacle_assembler.convert_obstacles_from_json(
            [VALID_OBSTACLE_JSON])

        self.position_assembler.convert_position_from_json.assert_called_once_with(
            VALID_OBSTACLE_JSON["position"])
        self.dimension_assembler.convert_dimension_from_json.assert_called_once_with(
            VALID_OBSTACLE_JSON["dimension"])

    def test_given_two_obstacles_scaling_when_convert_from_json_then_called_position_and_dimension(
            self):
        self.position_assembler.convert_position_from_json.side_effect = [
            Mock(pos_x=56, pos_y=80), Mock(pos_x=80, pos_y=20)
        ]
        self.dimension_assembler.convert_dimension_from_json.side_effect = [(
            7, 7), (9, 9)]
        obstacle_assembler = ObstacleAssembler(self.position_assembler,
                                               self.dimension_assembler)
        obstacles = obstacle_assembler.convert_obstacles_from_json(
            [VALID_OBSTACLE_JSON, VALID_OBSTACLE2_JSON])

        expected_position_calls = [
            call(VALID_OBSTACLE_JSON["position"]),
            call(VALID_OBSTACLE2_JSON["position"])
        ]
        expected_dimension_calls = [
            call(VALID_OBSTACLE_JSON["dimension"]),
            call(VALID_OBSTACLE2_JSON["dimension"])
        ]
        self.position_assembler.convert_position_from_json.assert_has_calls(
            expected_position_calls)
        self.dimension_assembler.convert_dimension_from_json.assert_has_calls(
            expected_dimension_calls)

    def test_given_one_obstacle_scaling_when_convert_from_json_then_return_proper_tag(
            self):
        self.setup_simple_obstacle()
        obstacle_assembler = ObstacleAssembler(self.position_assembler,
                                               self.dimension_assembler)

        obstacles = obstacle_assembler.convert_obstacles_from_json(
            [VALID_OBSTACLE_JSON])

        self.assertEqual(1, len(obstacles))
        self.assertEqual(LEFT, obstacles[0].tag)

    def test_given_two_obstacles_scaling_when_convert_from_json_then_return_proper_tag(
            self):
        self.setup_multiple_obstacles()
        obstacle_assembler = ObstacleAssembler(self.position_assembler,
                                               self.dimension_assembler)

        obstacles = obstacle_assembler.convert_obstacles_from_json(
            [VALID_OBSTACLE_JSON, VALID_OBSTACLE2_JSON])

        self.assertEqual(2, len(obstacles))
        self.assertEqual(LEFT, obstacles[0].tag)
        self.assertEqual(RIGHT, obstacles[1].tag)

    def test_given_one_obstacle_scaling_when_convert_from_json_then_radius_is_good(
            self):
        self.setup_simple_obstacle()
        obstacle_assembler = ObstacleAssembler(self.position_assembler,
                                               self.dimension_assembler)

        obstacles = obstacle_assembler.convert_obstacles_from_json(
            [VALID_OBSTACLE_JSON])

        self.assertEqual(FIRST_RADIUS, obstacles[0].radius)

    def test_given_two_obstacle_scaling_when_convert_from_json_then_radius_are_good(
            self):
        self.setup_multiple_obstacles()
        obstacle_assembler = ObstacleAssembler(self.position_assembler,
                                               self.dimension_assembler)

        obstacles = obstacle_assembler.convert_obstacles_from_json(
            [VALID_OBSTACLE_JSON, VALID_OBSTACLE2_JSON])

        self.assertEqual(FIRST_RADIUS, obstacles[0].radius)
        self.assertEqual(SECOND_RADIUS, obstacles[1].radius)

    def setup_multiple_obstacles(self):
        self.position_assembler.convert_position_from_json.side_effect = [
            Mock(pos_x=56, pos_y=80), Mock(pos_x=80, pos_y=20)
        ]
        self.dimension_assembler.convert_dimension_from_json.side_effect = [(
            FIRST_RADIUS * 2,
            FIRST_RADIUS * 2), (SECOND_RADIUS * 2, SECOND_RADIUS * 2)]

    def setup_simple_obstacle(self):
        self.position_assembler.convert_position_from_json.return_value = Mock(
            pos_x=56, pos_y=80)
        self.dimension_assembler.convert_dimension_from_json.return_value = (
            FIRST_RADIUS * 2, FIRST_RADIUS * 2)
