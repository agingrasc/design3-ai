import math

from domain.gameboard.gameboard import GameBoard
from domain.pathfinding import pathfinding
from mcu.commands import Move
from robot.task.task import Task


class GoToDrawzoneTask(Task):
    def __init__(self, robot_controller):

        Task.__init__(self, robot_controller)
        self.x_drawzone = 5
        self.y_drawzone = 5
        self.x_robot_position = 20
        self.y_robot_position = 40
        self.theta = -(math.pi / 2)
        self.status_flag = 0

    def execute(self, x_robot_position, y_robot_position):
        print("going to drawzone")
        self.y_robot_position = y_robot_position
        self.x_robot_position = x_robot_position
        self._find_path()
        self._go_to_drawzone()
        self._stop()
        return self.robot_controller

    def _find_path(self):
        game_board = GameBoard(50, 50, [])

        end_position = game_board.game_board[self.x_drawzone][self.y_drawzone]
        begin_position = game_board.game_board[self.x_robot_position][self.y_robot_position]

        pathfinder = pathfinding.PathFinding(game_board, begin_position,
                                             end_position)

        self.segments = pathfinder.find_path()

        game_board.print_game_board()

    def _go_to_drawzone(self):
        print("going to drawzone Command")
        for segment in self.segments:
            while self._distance(self.x_robot_position, self.y_robot_position, segment[0], segment[1]) <= 2:
                cmd = Move(segment[0], segment[1], self.theta)
                self.robot_controller.send_command(cmd)

    def _stop(self):
        self.status_flag = 1

