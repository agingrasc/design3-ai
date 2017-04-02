from domain.gameboard.position import Position


class Blackboard:
    def __init__(self):
        self.antenna_position: Position = None
        self.id_image = None
        self.magnification = None
        self.orientation = None
        self.segments_image = None

    def get_image_segments(self):
        return self.segments_image

    def get_image_id(self):
        return self.id_image
