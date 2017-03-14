import math

from domain.gameboard.gameboard import GameBoard
from domain.pathfinding import pathfinding
from mcu.commands import Move
from .task import Task


class GoToImageTask(Task):
    def __init__(self, robot_controller):
        Task.__init__(self, robot_controller)
        self.x_image = 20
        self.y_image = 40
        self.x_robot_position = 0
        self.y_robot_position = 0
        self.theta = -(math.pi/2)
        self.status_flag = 0
        self.images = {1: (5, 40), 2: (10, 40), 3: (15,40), 4: (20, 40)
                 , 5: (25, 40), 6: (30, 40), 7: (35, 40), 8: (40, 40)}

    def execute(self, x_robot_position, y_robot_position):
        print("going to image")
        print(self.id_image)
        print(self.magnification)
        print(self.orientation)
        self.y_robot_position = y_robot_position
        self.x_robot_position = x_robot_position
        self._find_path()
        self._go_to_image()
        self._stop()
        return self.robot_controller

    def _find_path(self):
        self.x_image = self.images[self.id_image][0]
        self.y_image = self.images[self.id_image][1]

        game_board = GameBoard(50, 50, [])

        end_position = game_board.game_board[self.x_image][self.y_image]
        begin_position = game_board.game_board[self.x_robot_position][self.y_robot_position]

        pathfinder = pathfinding.PathFinding(game_board, begin_position,
                                             end_position)

        self.segments = pathfinder.find_path()

        game_board.print_game_board()

    def _go_to_image(self):
        print("going to image Command")
        print(self.x_image)
        print(self.y_image)

        for segment in self.segments:
            while self._distance(self.x_robot_position, self.y_robot_position, segment[0], segment[1]) <= 2:
                cmd = Move(segment[0], segment[1], self.theta)
                self.robot_controller.send_command(cmd)

    def _stop(self):
        self.status_flag = 1