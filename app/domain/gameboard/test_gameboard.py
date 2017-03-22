import unittest
from domain.gameboard import gameboard

VALID_ROBOT_X_POSITION = 22
VALID_ROBOT_Y_POSITION = 11
VALID_OBSTACLE_X_POSITION = 15
VALID_OBSTACLE_Y_POSITION = 7
VALID_MAX_X = 30
VALID_MAX_Y = 15
VALID_RADIUS = 3


class GameBoardTest(unittest.TestCase):
    def test_init_pos_unique(self):
        board = gameboard.GameBoard(VALID_MAX_X, VALID_MAX_Y, [], 0)

        for i in range(0, VALID_MAX_X):
            for j in range(0, VALID_MAX_Y):
                coord = board.game_board[i][j]
                self.assertEqual(i, coord.pos_x)
                self.assertEqual(j, coord.pos_y)

    def test_set_notag_obstacle(self):
        obstacle = gameboard.ObstacleValueObject(
            pos_x=VALID_OBSTACLE_X_POSITION,
            pos_y=VALID_OBSTACLE_Y_POSITION,
            radius=VALID_RADIUS,
            tag='')
        board = gameboard.GameBoard(VALID_MAX_X, VALID_MAX_Y, [obstacle], 0)

        max_y = VALID_OBSTACLE_Y_POSITION + VALID_RADIUS - 1
        min_y = VALID_OBSTACLE_Y_POSITION - VALID_RADIUS - 1
        lim_y = VALID_OBSTACLE_Y_POSITION + VALID_RADIUS

        coord_max_y = board.game_board[VALID_OBSTACLE_X_POSITION][max_y]
        coord_min_y = board.game_board[VALID_OBSTACLE_X_POSITION][min_y]
        coord_lim_y = board.game_board[VALID_OBSTACLE_X_POSITION][lim_y]

        self.assertEqual(gameboard.Tag.CAN_PASS, coord_min_y.get_tag())
        self.assertEqual(gameboard.Tag.OBSTACLE, coord_max_y.get_tag())
        self.assertEqual(gameboard.Tag.CAN_PASS, coord_lim_y.get_tag())

    def test_set_left_obstacle(self):
        obstacle = gameboard.ObstacleValueObject(
            pos_x=VALID_OBSTACLE_X_POSITION,
            pos_y=VALID_OBSTACLE_Y_POSITION,
            radius=VALID_RADIUS,
            tag=gameboard.Tag.CANT_PASS_LEFT)
        board = gameboard.GameBoard(VALID_MAX_X, VALID_MAX_Y, [obstacle], 0)

        max_y = VALID_OBSTACLE_Y_POSITION + VALID_RADIUS - 1
        min_y = VALID_OBSTACLE_Y_POSITION - VALID_RADIUS - 1
        lim_y = VALID_OBSTACLE_Y_POSITION + VALID_RADIUS

        coord_max_y = board.game_board[VALID_OBSTACLE_X_POSITION][max_y]
        coord_min_y = board.game_board[VALID_OBSTACLE_X_POSITION][min_y]
        coord_lim_y = board.game_board[VALID_OBSTACLE_X_POSITION][lim_y]

        self.assertEqual(gameboard.Tag.OBSTACLE, coord_min_y.get_tag())
        self.assertEqual(gameboard.Tag.OBSTACLE, coord_max_y.get_tag())
        self.assertEqual(gameboard.Tag.CAN_PASS, coord_lim_y.get_tag())

    def test_set_right_obstacle(self):
        obstacle = gameboard.ObstacleValueObject(
            pos_x=VALID_OBSTACLE_X_POSITION,
            pos_y=VALID_OBSTACLE_Y_POSITION,
            radius=VALID_RADIUS,
            tag=gameboard.Tag.CANT_PASS_RIGHT)
        board = gameboard.GameBoard(VALID_MAX_X, VALID_MAX_Y, [obstacle], 0)

        max_y = VALID_OBSTACLE_Y_POSITION + VALID_RADIUS - 1
        min_y = VALID_OBSTACLE_Y_POSITION - VALID_RADIUS - 1
        lim_y = VALID_OBSTACLE_Y_POSITION + VALID_RADIUS

        coord_max_y = board.game_board[VALID_OBSTACLE_X_POSITION][max_y]
        coord_min_y = board.game_board[VALID_OBSTACLE_X_POSITION][min_y]
        coord_lim_y = board.game_board[VALID_OBSTACLE_X_POSITION][lim_y]

        self.assertEqual(gameboard.Tag.CAN_PASS, coord_min_y.get_tag())
        self.assertEqual(gameboard.Tag.OBSTACLE, coord_max_y.get_tag())
        self.assertEqual(gameboard.Tag.OBSTACLE, coord_lim_y.get_tag())

    def test_set_right_obstacle_with_robot_radius(self):
        obstacle = gameboard.ObstacleValueObject(
            pos_x=VALID_OBSTACLE_X_POSITION,
            pos_y=VALID_OBSTACLE_Y_POSITION,
            radius=VALID_RADIUS - 1,
            tag=gameboard.Tag.CANT_PASS_RIGHT)
        board = gameboard.GameBoard(VALID_MAX_X, VALID_MAX_Y, [obstacle], 1)

        max_y = VALID_OBSTACLE_Y_POSITION + VALID_RADIUS - 1
        min_y = VALID_OBSTACLE_Y_POSITION - VALID_RADIUS - 1
        lim_y = VALID_OBSTACLE_Y_POSITION + VALID_RADIUS

        coord_max_y = board.game_board[VALID_OBSTACLE_X_POSITION][max_y]
        coord_min_y = board.game_board[VALID_OBSTACLE_X_POSITION][min_y]
        coord_lim_y = board.game_board[VALID_OBSTACLE_X_POSITION][lim_y]

        self.assertEqual(gameboard.Tag.CAN_PASS, coord_min_y.get_tag())
        self.assertEqual(gameboard.Tag.OBSTACLE, coord_max_y.get_tag())
        self.assertEqual(gameboard.Tag.OBSTACLE, coord_lim_y.get_tag())

    def test_set_left_obstacle_with_robot_radius(self):
        obstacle = gameboard.ObstacleValueObject(
            pos_x=VALID_OBSTACLE_X_POSITION,
            pos_y=VALID_OBSTACLE_Y_POSITION,
            radius=VALID_RADIUS - 1,
            tag=gameboard.Tag.CANT_PASS_LEFT)
        board = gameboard.GameBoard(VALID_MAX_X, VALID_MAX_Y, [obstacle], 1)

        max_y = VALID_OBSTACLE_Y_POSITION + VALID_RADIUS - 1
        min_y = VALID_OBSTACLE_Y_POSITION - VALID_RADIUS - 1
        lim_y = VALID_OBSTACLE_Y_POSITION + VALID_RADIUS

        coord_max_y = board.game_board[VALID_OBSTACLE_X_POSITION][max_y]
        coord_min_y = board.game_board[VALID_OBSTACLE_X_POSITION][min_y]
        coord_lim_y = board.game_board[VALID_OBSTACLE_X_POSITION][lim_y]

        self.assertEqual(gameboard.Tag.OBSTACLE, coord_min_y.get_tag())
        self.assertEqual(gameboard.Tag.OBSTACLE, coord_max_y.get_tag())
        self.assertEqual(gameboard.Tag.CAN_PASS, coord_lim_y.get_tag())

    def test_set_notag_obstacle_with_robot_radius(self):
        obstacle = gameboard.ObstacleValueObject(
            pos_x=VALID_OBSTACLE_X_POSITION,
            pos_y=VALID_OBSTACLE_Y_POSITION,
            radius=VALID_RADIUS - 2,
            tag='')
        board = gameboard.GameBoard(VALID_MAX_X, VALID_MAX_Y, [obstacle], 2)

        max_y = VALID_OBSTACLE_Y_POSITION + VALID_RADIUS - 1
        min_y = VALID_OBSTACLE_Y_POSITION - VALID_RADIUS - 1
        lim_y = VALID_OBSTACLE_Y_POSITION + VALID_RADIUS

        coord_max_y = board.game_board[VALID_OBSTACLE_X_POSITION][max_y]
        coord_min_y = board.game_board[VALID_OBSTACLE_X_POSITION][min_y]
        coord_lim_y = board.game_board[VALID_OBSTACLE_X_POSITION][lim_y]

        self.assertEqual(gameboard.Tag.CAN_PASS, coord_min_y.get_tag())
        self.assertEqual(gameboard.Tag.OBSTACLE, coord_max_y.get_tag())
        self.assertEqual(gameboard.Tag.CAN_PASS, coord_lim_y.get_tag())
