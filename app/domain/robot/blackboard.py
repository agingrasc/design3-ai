from typing import Dict

from domain.gameboard.position import Position

POSITIONS = [
    Position(1959, 366, 1.57), Position(2024, 305, 1.22), Position(1933, 267, 0.35), Position(1890, 360, 0.00),
    Position(1929, 615, 0), Position(1940, 750, -0.20), Position(2096, 551, -1.37), Position(2005, 580, -1.75)
]


class Blackboard:
    def __init__(self):
        self.antenna_position: Position = None
        self.id_image = None
        self.magnification = None
        self.orientation = None
        self.segments_image = None
        self.images_position: Dict[int, Position] = {
            0: POSITIONS[0],
            1: POSITIONS[1],
            2: POSITIONS[2],
            3: POSITIONS[3],
            4: POSITIONS[4],
            5: POSITIONS[5],
            6: POSITIONS[6],
            7: POSITIONS[7],
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
