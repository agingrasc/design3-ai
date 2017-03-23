from api.gotoposition.positionassembler import PositionAssembler
from api.gotoposition.dimensionassembler import DimensionAssembler
from domain.gameboard.gameboard import ObstacleValueObject
from typing import List


class ObstacleAssembler:
    def __init__(self,
                 position_assembler: PositionAssembler,
                 dimension_assembler: DimensionAssembler,
                 scaling=1):
        self.scaling = scaling
        self.position_assembler = position_assembler
        self.dimension_assembler = dimension_assembler

    def convert_obstacles_from_json(self, obstacles) -> List:
        new_obstacles = []
        for obstacle in obstacles:
            position = self.position_assembler.convert_position_from_json(
                obstacle["position"])
            dimension = self.dimension_assembler.convert_dimension_from_json(
                obstacle["dimension"])
            tag = obstacle["tag"]
            new_obstacle = ObstacleValueObject(
                pos_x=position.pos_x,
                pos_y=position.pos_y,
                tag=tag,
                radius=int(dimension[0] / 2))
            new_obstacles.append(new_obstacle)
        return new_obstacles
