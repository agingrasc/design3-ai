from domain.gameboard.position import Position
from mcu.robotcontroller import RobotController
from service.globalinformation import GlobalInformation


START_POSITION = Position(310, 865, 2.356)
STOP_POSITION = Position(1280, 865, 2.356)
LINE_SEGMENT_SIZE = 10


class Antenna:
    def __init__(self, global_information: GlobalInformation, robot_controler: RobotController):
        self.robot_controler = robot_controler
        self.global_information = global_information

    def start_recording(self):
        self.robot_controler.start_power_recording()

    def end_recording(self):
        self.robot_controler.stop_power_recording()

    def get_max_signal_position(self) -> Position:
        return self.robot_controler.get_max_power_position()

    def get_start_antenna_position(self) -> Position:
        return START_POSITION

    def get_end_antenna_position(self) -> Position:
        return STOP_POSITION

    def get_segment_max_signal_antenna(self, position) -> Position:
        return Position(position.pos_x, position.pos_y - LINE_SEGMENT_SIZE, position.theta)
