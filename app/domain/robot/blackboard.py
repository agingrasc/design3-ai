from domain.gameboard.position import Position


class Blackboard:
    def __init__(self):
        self.antenna_position: Position = None
        self.id_image = None
        self.magnification = None
        self.orientation = None
        self.segments_image = None

    def get_segments_image():
        return self.segments_image

    def get_id_image():
        return self.id_image
