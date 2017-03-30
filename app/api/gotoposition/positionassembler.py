from domain.gameboard.position import Position


class PositionAssembler:
    def __init__(self, scaling=1):
        self.scaling = scaling

    def convert_position_from_json(self, position) -> Position:
        try:
            x_position = int(float(position["x"]) / self.scaling)
            y_position = int(float(position["y"]) / self.scaling)
        except:
            x_position = -1000
            y_position = -1000
        try:
            theta = float(position["theta"])
            return Position(x_position, y_position, theta)
        except:
            return Position(x_position, y_position)
