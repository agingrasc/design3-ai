from typing import Dict

from domain.gameboard.position import Position


class Blackboard:
    def __init__(self):
        self.antenna_position: Position = None
        self.id_image = None
        self.magnification = None
        self.orientation = None
        self.segments_image = None
        self.images_position: Dict[int, Position] = {
            0: Position(1895, 330, 1.52),
            1: Position(1910, 290, 1.00),
            2: Position(1910, 250, 0.37),
            3: Position(1895, 330, 0.00),
            4: Position(1900, 560, 0.00),
            5: Position(1910, 635, -0.50),
            6: Position(1910, 630, -1.05),
            7: Position(1910, 605, -1.54)
        }

    def get_image_segments(self):
        self.segments_image += [self.segments_image[0]]
        return self.segments_image

    def get_image_id(self):
        return self.id_image

    def get_image_position(self, image_id):
        return self.images_position[image_id]
      
    def has_antenna_position(self):
        if self.antenna_position:
            return True
        else:
            return False

    def get_antenna_position(self):
        return self.antenna_position

    def get_segment_image_list(self):
        return self.segments_image

