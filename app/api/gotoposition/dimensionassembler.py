from typing import Tuple


class DimensionAssembler:
    def __init__(self, scaling=1):
        self.scaling = scaling

    def convert_dimension_from_json(self, dimension) -> Tuple:
        width = int(float(dimension["width"]) / self.scaling)
        length = int(float(dimension["length"]) / self.scaling)
        return (width, length)
