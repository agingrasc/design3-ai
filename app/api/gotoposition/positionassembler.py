from domain.gameboard.position import Position


class PositionAssembler:
    def __init__(self, scaling=1):
        self.scaling = scaling

    def convert_position_from_json(self, position) -> Position:
        x_position = int(float(position["x"]) / self.scaling)
        y_position = int(float(position["y"]) / self.scaling)
        theta = float(position["theta"])
        return Position(x_position, y_position, theta)
