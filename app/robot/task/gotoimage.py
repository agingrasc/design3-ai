import math

from domain.gameboard.gameboard import GameBoard
from domain.pathfinding import pathfinding
from mcu.commands import Move
from .task import task


class go_to_image(task):
    def __init__(self, robot_controller):
        task.__init__(self, robot_controller)
        self.x_image = 20
        self.y_image = 40
        self.x_robot_position = 0
        self.y_robot_position = 0
        self.theta = -(math.pi/2)
        self.next_state = self._go_to_image
        self.status_flag = 0
        self.robot_controller = None

    def execute(self, x_robot_position, y_robot_position):
        print("going to image")
        print(self.id_image)
        print(self.magnification)
        print(self.orientation)
        self.y_robot_position = y_robot_position
        self.x_robot_position = x_robot_position
        self.next_state()
        return self.robot_controller

    def _go_to_image(self):
        print("going to image Command")
        print(self.x_image)
        print(self.y_image)

        game_board = GameBoard(50, 50, [])

        end_position = game_board.game_board[self.x_image][self.y_image]
        begin_position = game_board.game_board[self.x_robot_position][self.y_robot_position]

        pathfinder = pathfinding.PathFinding(game_board, begin_position,
                                             end_position)

        path = pathfinder.find_path()
        segments = self._get_segments_path(path)

        game_board.print_game_board()

        for segment in segments:
            while self._distance(self.x_robot_position, self.y_robot_position, segment[0], segment[1]) <= 2:
                # testGit
                cmd = Move(segment[0], segment[1], self.theta)
                self.robot_controller.send_command(cmd)

        self.x_robot_position = segments[len(segments)-1][0]
        self.y_robot_position = segments[len(segments)-1][1]

        if self._distance(self.x_robot_position, self.y_robot_position, self.x_image, self.y_image) <= 2:
            self.next_state = self._stop()


    def _stop(self):
        self.status_flag = 1

    def _get_segments_path(self, path):
        segments = []
        x_segment = path[0].pos_x
        y_segment = path[0].pos_y
        for i in range(1, (len(path) - 1)):
            if path[i].pos_x == x_segment & path[i].pos_y != y_segment:
                y_segment = path[i].pos_y

                if path[i].pos_x != path[(i + 1)].pos_x:
                    segments.append((x_segment, y_segment))
            elif path[i].pos_y == y_segment & path[i].pos_x != x_segment:
                x_segment = path[i].pos_x
                if path[i].pos_y != path[(i + 1)].pos_y:
                    segments.append((x_segment, y_segment))
            else:
                x_segment = path[i].pos_x
                y_segment = path[i].pos_y
                if path[i].pos_x == path[(i + 1)].pos_x | path[i].pos_y == path[(i + 1)].pos_y:
                    segments.append((x_segment, y_segment))

        segments.append((x_segment, y_segment))
        return segments

    def _distance(self, x_point1, y_point1, x_point2, y_point2):
        return math.sqrt((x_point1 - x_point2) ** 2 + (y_point1 - y_point2) ** 2)