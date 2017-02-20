from gameboard.position import Position
from robot.robot import Robot
from robot.task.task import Task
from gameboard import gameboard
from .mockrobot.task.mockmovingrobotaction import MockMovingRobotAction
from .mockrobot.wheel.wheelservice import MockWheelService

VALID_MAX_X = 50
VALID_MAX_Y = 100
VALID_ROBOT_X_POSITION = 1
VALID_ROBOT_Y_POSITION = 1


class Simulator:



    def __init__(self):
        pass

    def start(self):
        print("Starting simulator...")
        wheel_service = MockWheelService()
        robot = Robot()

        task = Task()
        next_position = Position(10, 100)

        task.register(MockMovingRobotAction(next_position, wheel_service))

        robot.execute_task(task)

    def simulate_going_to_position(self, pos_x, pos_y):
        self.obstacle_builder = gameboard.ObstacleBuilder()
        board = gameboard.GameBoard(VALID_MAX_X, VALID_MAX_Y, self.obstacle_builder)
        board.set_robot_position(VALID_ROBOT_X_POSITION, VALID_ROBOT_Y_POSITION)
        board.print_game_board()
        changing_pos_x = VALID_ROBOT_X_POSITION
        changing_pos_y = VALID_ROBOT_Y_POSITION
        print("I m in position (" + str(changing_pos_x) + ", " + str(changing_pos_y) + ")")
        print("printing déplacement en y")
        while (changing_pos_y != int(pos_y)):
            if(changing_pos_y > int(pos_y)):
                changing_pos_y -= 1
            elif(changing_pos_y < int(pos_y)):
                changing_pos_y += 1
            print("I m in position (" + str(changing_pos_x) + ", " + str(changing_pos_y) + ")")
            board.set_robot_position(changing_pos_x, changing_pos_y)
            board.print_game_board()


        print("printing déplacement en x")
        while(changing_pos_x != int(pos_x)):
            if (changing_pos_x > int(pos_x)):
                changing_pos_x -= 1
            elif (changing_pos_x < int(pos_x)):
                changing_pos_x += 1

            print("I m in position (" + str(changing_pos_x) + ", " + str(changing_pos_y) + ")")
            board.set_robot_position(changing_pos_x, changing_pos_y)
            board.print_game_board()


