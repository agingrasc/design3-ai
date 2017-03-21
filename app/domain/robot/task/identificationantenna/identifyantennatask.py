import math

from domain.robot.task.task import Task
from domain.robot.feedback import Feedback
from service.globalinformation import GlobalInformation
from domain.command.visionregulation import VisionRegulation
from domain.command.drawer import Drawer
from domain.gameboard.position import Position
from domain.command.antenna import Antenna

X_START_OFFSET = 0
Y_OFFSET = 15

X_END_OFFSET = 50
LINE_LENGHT = 1


class IdentifyAntennaTask(Task):
    def __init__(self,
                 drawer: Drawer,
                 antenna: Antenna,
                 feedback: Feedback,
                 vision_regulation: VisionRegulation,
                 global_information: GlobalInformation):
        self.drawer = drawer
        self.antenna = antenna
        self.vision_regulation = vision_regulation
        self.global_information = global_information
        self.feedback = feedback

    def execute(self):
        self.vision_regulation.go_to_position(
            self.antenna.get_start_antenna_position())
        self.antenna.start_recording()
        self.vision_regulation.go_to_position(
            self.antenna.get_end_antenna_position())
        self.antenna.end_recording()
        self.draw_line()

        self.feedback.send_comment("End identifying antenna")

    def draw_line(self):
        max_signal_position = self.antenna.get_max_signal_position()
        self.vision_regulation.go_to_position(max_signal_position)
        end_position_x = max_signal_position.pos_x
        end_position_y = max_signal_position.pos_y
        end_position = Position(end_position_x, end_position_y + LINE_LENGHT)
        self.drawer.draw([max_signal_position, end_position])
