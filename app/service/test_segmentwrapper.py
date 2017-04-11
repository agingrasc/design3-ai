from unittest import TestCase
from unittest.mock import Mock

from domain.gameboard.position import Position
from service.segmentwrapper import SegmentWrapper

VALID_SEGMENT_LIST = [Position(pos_x=0, pos_y=0), Position(pos_x=200, pos_y=200), Position(pos_x=210, pos_y=210)]
ADDED_POSITION = Position(pos_x=100, pos_y=100)

class SegmentWrapperTest(TestCase):
    def setUp(self):
       self.blackboard = Mock()
       self.blackboard.get_segment_image_list.return_value = VALID_SEGMENT_LIST

    def test_return_segmentation_wrapped_correctly(self):
       segment_wrapper = SegmentWrapper(self.blackboard)

       list_segment = segment_wrapper.wrap_segment()

       self.assertEquals(len(list_segment), 4)
       self.assertTrue(list_segment[0] == Position(pos_x=0, pos_y=0))
       self.assertTrue(list_segment[1] == ADDED_POSITION)
       self.assertTrue(list_segment[2] == Position(pos_x=200, pos_y=200))
       self.assertTrue(list_segment[3] == Position(pos_x=210, pos_y=210))

