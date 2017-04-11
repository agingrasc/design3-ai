from unittest import TestCase
from unittest.mock import Mock
from service.safezonefinder import SafeZoneFinder
from service.safezonefinder import STOP_POSITION_LIST
from domain.gameboard.position import Position

STOP_POSITION_LIST = [Position(1250, 580, 0), Position(1250, 880, 0)]

VALID_PATH_1 = [Mock(), STOP_POSITION_LIST[0]]
NOT_VALID_PATH_1 = [Mock(), Mock()]
VALID_PATH_2 = [Mock(), Mock(), STOP_POSITION_LIST[1]]
NOT_VALID_PATH_2 = [Mock(), Mock(), Mock()]

NOT_FLOOR_POSITION = [Position(1255, 588)]
FLOOR_POSITION = [Position(1250, 580)]


class SafeZoneFinderTest(TestCase):
    def setUp(self):
        self.pathfinding_application_service = Mock()
        self.global_information = Mock()
        self.safe_zone_finder_test = SafeZoneFinder(self.pathfinding_application_service, self.global_information)

    def test_find_shorter_safe_zone_2_valid_paths(self):
        self.pathfinding_application_service.find.side_effect = [VALID_PATH_1, VALID_PATH_2]
        path = self.safe_zone_finder_test.find_safe_zone(STOP_POSITION_LIST)
        self.assertEqual(VALID_PATH_1, path)

    def test_find_shorter_safe_zone_1_valid_path1(self):
        self.pathfinding_application_service.find.side_effect = [VALID_PATH_1, NOT_VALID_PATH_2]
        path = self.safe_zone_finder_test.find_safe_zone(STOP_POSITION_LIST)
        self.assertEqual(VALID_PATH_1, path)

    def test_find_shorter_safe_zone_1_valid_path2(self):
        self.pathfinding_application_service.find.side_effect = [NOT_VALID_PATH_1, VALID_PATH_2]
        path = self.safe_zone_finder_test.find_safe_zone(STOP_POSITION_LIST)
        self.assertEqual(VALID_PATH_2, path)

    def test_find_not_floor_position(self):
        self.pathfinding_application_service.find.side_effect = [FLOOR_POSITION]
        path = self.safe_zone_finder_test.find_safe_zone(NOT_FLOOR_POSITION)
        self.assertEqual(FLOOR_POSITION, path)

    def test_find_two_times(self):
        self.pathfinding_application_service.find.side_effect = [FLOOR_POSITION, NOT_VALID_PATH_1, VALID_PATH_2]

        path_1 = self.safe_zone_finder_test.find_safe_zone(NOT_FLOOR_POSITION)
        path_2 = self.safe_zone_finder_test.find_safe_zone(STOP_POSITION_LIST)

        self.assertEqual(FLOOR_POSITION, path_1)
        self.assertEqual(VALID_PATH_2, path_2)
