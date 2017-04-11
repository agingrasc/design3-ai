from unittest import TestCase
from unittest.mock import Mock
from service.safezonefinder import SafeZoneFinder
from service.safezonefinder import STOP_POSITION_LIST

VALID_PATH_1 = [
    4,
    6,
    7,
    STOP_POSITION_LIST[0],
]
VALID_PATH_2 = [
    2,
    3,
    4,
    6,
    7,
    STOP_POSITION_LIST[1],
]


class SafeZoneFinderTest(TestCase):
    def setUp(self):
        self.pathfinding_application_service = Mock()
        self.global_information = Mock()
        self.safe_zone_finder_test = SafeZoneFinder(self.pathfinding_application_service, self.global_information)

    def test_find_shorter_safe_zone_2_valid_paths(self):
        self.pathfinding_application_service.find.side_effect = [VALID_PATH_1, VALID_PATH_2, [], []]
        path = self.safe_zone_finder_test.find_safe_zone()
        self.assertEqual(VALID_PATH_1, path)

    def test_find_shorter_safe_zone_1_valid_path(self):
        self.pathfinding_application_service.find.side_effect = [[], VALID_PATH_2, [], []]
        path = self.safe_zone_finder_test.find_safe_zone()
        self.assertEqual(VALID_PATH_2, path)
