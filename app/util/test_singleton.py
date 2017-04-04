import unittest

from util.singleton import MockForSingleton


class TestSingleton(unittest.TestCase):

    def setUp(self):
        self.singleton = MockForSingleton()
        self.singleton.first_value = 0
        self.singleton.second_value = 0

    def tearDown(self):
        pass

    def test_one_singleton(self):
        self.singleton.first_value = 1
        self.assertEqual(1, self.singleton.first_value)
        self.assertEqual(0, self.singleton.second_value)

    def test_two_singleton(self):
        self.singleton.first_value = 1
        self.assertEqual(1, self.singleton.first_value)
        self.assertEqual(0, self.singleton.second_value)

        second_singleton = MockForSingleton()
        self.assertEqual(1, second_singleton.first_value)
        second_singleton.second_value = 2
        self.assertEqual(2, self.singleton.second_value)

    def test_multiples_singleton(self):
        second_singleton = MockForSingleton()
        third_singleton = MockForSingleton()
        self.assertEqual(self.singleton.first_value, second_singleton.first_value)
        self.assertEqual(self.singleton.first_value, third_singleton.first_value)

        second_singleton.first_value = 1
        self.assertEqual(self.singleton.first_value, second_singleton.first_value)
        self.assertEqual(self.singleton.first_value, third_singleton.first_value)

        third_singleton.first_value = 2
        self.assertEqual(self.singleton.first_value, second_singleton.first_value)
        self.assertEqual(self.singleton.first_value, third_singleton.first_value)
