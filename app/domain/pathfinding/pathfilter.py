from typing import List

from domain.gameboard.position import Position


class PathFilter:



    def get_corner_from_path(self, path: List[Position]):
        if len(path) <= 2:
            return path
        i = 1
        last_angle = self.get_angle(path[i], path[0])
        i += 1
        angle = self.get_angle(path[i], path[0])
        while angle == last_angle and i + 1 < len(path):
            i += 1
            angle = self.get_angle(path[i], path[0])
        initial_pos = path[0]
        rest = path[i:]
        return [initial_pos] + self.get_corner_from_path(rest)

    def get_angle(self, pos1: Position, pos2: Position):
        vector = Position(pos1.pos_x - pos2.pos_x, pos1.pos_y - pos2.pos_y)
        return vector.get_angle()

    def filter_path(self, path: List[Position], target: Position) -> List[Position]:
        segments = []
        segments.append(path[0])

        for i in range(1, (len(path) - 1)):
            if (path[i].pos_x - segments[len(segments) - 1].pos_x > 40) or (path[i].pos_y - segments[len(segments) - 1].pos_y > 40 ):
                segments.append(path[i])
        del segments[0]
        segments.append(target)
        return segments


