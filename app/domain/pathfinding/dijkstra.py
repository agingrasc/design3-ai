from enum import Enum
import heapq

import math
from typing import List, Tuple

from domain.gameboard.position import Position
from domain.pathfinding.grid import Grid, Cell, ObstacleType
from domain.pathfinding.pathfilter import PathFilter

"""https://joernhees.de/blog/2010/07/19/min-heap-in-python/"""
class Heap:
    """ A neat min-heap wrapper which allows storing items by priority
        and get the lowest item out first (pop()).
        Also implements the iterator-methods, so can be used in a for
        loop, which will loop through all items in increasing priority order.
        Remember that accessing the items like this will iteratively call
        pop(), and hence empties the heap! """

    def __init__(self):
        """ create a new min-heap. """
        self._heap = []

    def push(self, priority, item):
        """ Push an item with priority into the heap.
            Priority 0 is the highest, which means that such an item will
            be popped first."""
        assert priority >= 0
        heapq.heappush(self._heap, (priority, item))

    def pop(self):
        """ Returns the item with lowest priority. """
        item = heapq.heappop(self._heap)[1] # (prio, item)[1] == item
        return item

    def __len__(self):
        return len(self._heap)

    def __next__(self):
        return self.next()

    def next(self):
        """ Get all elements ordered by their priority (lowest first). """
        try:
            return self.pop()
        except IndexError:
            raise StopIteration


class NoPathFound(Exception):
    pass


class Dijkstra:
    def __init__(self, grid: Grid):
        self.heap = Heap()
        self.grid = grid
        self.path_filter = PathFilter()

    def get_path(self, robot_position: Position, target_position: Position) -> List[Position]:
        x, y = robot_position.pos_x , robot_position.pos_y
        init_cell = self.grid.get_cell(x, y)
        init_cell.update_weight(0)
        init_cell.mark_path()
        self.heap.push(init_cell.weight, init_cell)

        try:
            while True:
                work_cell = self.heap.pop()
                if work_cell.visited:
                    continue
                for neighbor in self.grid.get_neighbors(work_cell):
                    if not neighbor.visited and not neighbor.is_blocked():
                        neighbor.update_weight(work_cell.weight+1)
                        neighbor.previous = work_cell
                        self.heap.push(neighbor.weight, neighbor)
                work_cell.visited = True
        except IndexError:
            pass

        target_x, target_y = target_position.pos_x, target_position.pos_y
        target_cell = self.grid.get_cell(target_x, target_y)
        target_cell.mark_path()
        path = [target_cell]
        prev_cell: Cell = target_cell.previous

        try:
            while prev_cell is not init_cell:
                prev_cell.mark_path()
                path.append(prev_cell)
                prev_cell = prev_cell.previous
        except Exception as e:
            raise NoPathFound()

        path.reverse()

        final_path = [Position(int(point.i * self.grid.scale + self.grid.scale/2), int(point.j * self.grid.scale + self.grid.scale/2), robot_position.theta) for point in path]
        return final_path

    def get_segmented_path(self, robot, target):
        return self.path_filter.get_corner_from_path(self.get_path(robot, target))





def main():
    obs1 = Position(1000, 350), 140, ObstacleType.NORMAL
    obs2 = Position(1500, 600), 140, ObstacleType.PASS_BY_RIGHT
    test_grid = Grid(2300, 1120, 10, 150, [obs1, obs2])
    test_grid.print_grid()
    dijkstra = Dijkstra(test_grid)
    path_filter = PathFilter()
    path = dijkstra.get_segmented_path(Position(250, 250), Position(1900, 300))
    path_segments = path_filter.filter_path(path)
    for idx, pos in enumerate(path_segments):
        print("Pos ({}): {} -- {} -- {}\n".format(idx, pos.pos_x, pos.pos_y, pos.theta))
    test_grid.print_grid()


if __name__ == "__main__":
    main()
