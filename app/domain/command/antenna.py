from domain.gameboard.position import Position
from mcu.robotcontroller import RobotController
from service.globalinformation import GlobalInformation


START_POSITION = Position(260, 880, 0.785398) # 310, 865
STOP_POSITION = Position(1250, 880, 0.785398) # 1280, 865
MAX_Y = 870
LINE_SEGMENT_SIZE = 10


class Antenna:
    def __init__(self, global_information: GlobalInformation, robot_controler: RobotController):
        self.robot_controller = robot_controler
        self.global_information = global_information

    def start_recording(self):
        self.robot_controller.start_power_recording()

    def end_recording(self):
        self.robot_controller.stop_power_recording()

    def move_to_end_position(self):
        self.robot_controller.manual_move(STOP_POSITION, Position(20, 0))

    def get_max_signal_position(self) -> Position:
        pos = self.robot_controller.get_max_power_position()
        pos.pos_y = MAX_Y
        return pos

    def get_start_antenna_position(self) -> Position:
        return START_POSITION

    def get_stop_antenna_position(self) -> Position:
        return STOP_POSITION

    def get_segment_max_signal_antenna(self, position) -> Position:
        return Position(position.pos_x, position.pos_y - LINE_SEGMENT_SIZE, position.theta)
