import math

from domain.gameboard.position import Position
from domain.robot.blackboard import Blackboard

MIN_DISTANCE_PRECISION = 200

class SegmentWrapper():

    def __init__(self, blackboard: Blackboard):
        self.blackboard = blackboard

    def wrap_segment(self):
        segment_list = self.blackboard.get_segment_image_list()
        actual_position = segment_list[0]
        last_position = segment_list[len(segment_list)-1]


        while actual_position != last_position:
            i = 1
            if self._calculate_distance(actual_position, segment_list[i]) > MIN_DISTANCE_PRECISION:
                vector = segment_list[i] - actual_position
                half_vector = vector.multiply(0.5)

                new_position = actual_position + half_vector
                segment_list.insert(i, new_position)
                actual_position = segment_list[i+1]
                i = i+2
            else:
                actual_position = segment_list[i]
                i = i+1
        return segment_list




    def _calculate_distance(self, first_position: Position, second_position: Position):
            return math.sqrt((first_position.pos_x - second_position.pos_x) ** 2 + (first_position.pos_y - second_position.pos_y) ** 2)