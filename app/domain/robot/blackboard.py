from domain.gameboard.position import Position


class Blackboard:
    def __init__(self):
        self.antenna_position: Position = None
        self.id_image = None
        self.magnification = None
        self.orientation = None
        self.segments_image = None

    def get_image_segments(self):
        self.segments_image += [self.segments_image[0]]
        return self.segments_image

    def get_image_id(self):
        return self.id_image

    def has_antenna_position(self):
        if self.antenna_position:
            return True
        else:
            return False