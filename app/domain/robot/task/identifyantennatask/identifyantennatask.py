import math

from domain.robot.task.task import Task
from domain.robot.feedback import Feedback
from service.globalinformation import GlobalInformation
from domain.command.visionregulation import VisionRegulation
from domain.command.drawer import Drawer
from domain.gameboard.position import Position
from domain.command.antenna import Antenna

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
        start_position = self.antenna.get_start_antenna_position()
        self.vision_regulation.go_to_position(start_position)
        self.antenna.start_recording()
        end_position = self.antenna.get_end_antenna_position()
        self.vision_regulation.go_to_position(end_position)
        self.antenna.end_recording()
        self.draw_line()
        self.feedback.send_comment("End identifying antenna")

    def draw_line(self):
        max_signal_position = self.antenna.get_max_signal_position()
        self.vision_regulation.go_to_position(max_signal_position)
        end_position = self.antenna.get_segment_max_signal_antenna(
            max_signal_position)
        self.drawer.draw([max_signal_position, end_position])
