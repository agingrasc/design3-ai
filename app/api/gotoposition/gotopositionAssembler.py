from domain.gameboard.position import Position
from typing import Tuple


class GoToPositionAssembler:
    def __init__(self, scaling=1):
        self.scaling = scaling

    def convert_position_from_json(self, position) -> Position:
        x_position = int(float(position["x"]) / self.scaling)
        y_position = int(float(position["y"]) / self.scaling)
        return Position(x_position, y_position)

    def convert_dimension_from_json(self, dimension) -> Tuple:
        width = int(float(dimension["width"]) / self.scaling)
        lenght = int(float(dimension["lenght"]) / self.scaling)
        return (width, lenght)
