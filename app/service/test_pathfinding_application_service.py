from unittest import TestCase
from unittest.mock import Mock
from . import pathfinding_application_service
from domain.gameboard.position import Position

ROBOT_POSITION = Position(2170, 270)
BOARD_DIMENSIONS = 2300, 1110
OBSTACLE_JSON = [{"position": {"x": "149", "y": "170"}, "dimension": {"width": 20, "length": 20}, "tag": "LEFT"}]
ROBOT_RADIUS = 20


class PathFindingApplicationServiceTest(TestCase):
    def setUp(self):
        self.global_information = Mock()
        self.destination = Position(1080, 800)
        self.global_information.get_robot_position.return_value = ROBOT_POSITION
        self.global_information.get_board_dimensions.return_value = BOARD_DIMENSIONS
        self.global_information.get_obstacles_json.return_value = OBSTACLE_JSON
        self.global_information.get_robot_radius.return_value = ROBOT_RADIUS

    def test_call_correctly_global_information(self):
        pathfinding_application_service.find(self.global_information, self.destination)

        self.global_information.get_robot_position.assert_called_once()
        self.global_information.get_board_dimensions.assert_called_once()
        self.global_information.get_obstacles_json.assert_called_once()
        self.global_information.get_robot_radius.assert_called_once()

    def test_path_is_valid(self):
        path = pathfinding_application_service.find(self.global_information, self.destination)

        self.assertTrue(len(path) > 0)
