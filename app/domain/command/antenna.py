from domain.gameboard.position import Position
from service.globalinformation import GlobalInformation

X_START_OFFSET = 0
Y_OFFSET = 15
LINE_LENGHT = 1

X_END_OFFSET = 50


class Antenna:
    def __init__(self, global_information: GlobalInformation):
        self.global_information = global_information

    def start_recording(self):
        pass

    def end_recording(self):
        pass

    def get_max_signal_position(self) -> Position:
        pass

    def get_start_antenna_position(self) -> Position:
        robot_width = self.global_information.get_robot_width()
        x = X_START_OFFSET + (robot_width / 2) + 1
        y = Y_OFFSET + (robot_width / 2) + 1
        return Position(x, y)

    def get_end_antenna_position(self) -> Position:
        robot_width = self.global_information.get_robot_width()
        x = X_END_OFFSET + (robot_width / 2) + 1
        y = Y_OFFSET + (robot_width / 2) + 1
        return Position(x, y)

    def get_segment_max_signal_antenna(self, position) -> Position:
        return Position(position.pos_x, position.pos_y + LINE_LENGHT)
