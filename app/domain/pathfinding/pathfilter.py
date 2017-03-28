from typing import List

from domain.gameboard.position import Position


class PathFilter:
    def filter_path(self, path: List[Position]) -> List[Position]:
        segments = []
        segments.append(path[0])

        for i in range(1, (len(path) - 1)):
            if (path[i].pos_x - segments[len(segments) - 1].pos_x > 40) or (path[i].pos_y - segments[len(segments) - 1].pos_y > 40 ):
                segments.append(path[i])
        del segments[0]
        return segments
