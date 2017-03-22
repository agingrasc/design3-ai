from domain.command.antenna import Antenna
from domain.command.decoder import Decoder
from domain.command.visionregulation import VisionRegulation
from domain.robot.feedback import Feedback
from domain.robot.task.task import Task


class ReceiveInformationTask(Task):
    def __init__(self, antenna: Antenna,
                        feedback: Feedback,
                        vision_regulation: VisionRegulation,
                        decoder: Decoder):
        self.antenna = antenna
        self.feedback = feedback
        self.vision_regulation = vision_regulation
        self.decoder = decoder

    def execute(self):
        max_signal_position = self.antenna.get_max_signal_position()
        self.vision_regulation.go_to_position((max_signal_position))
        self.decoder.decode_information()
        self.id_image = self.decoder.get_image_number()
        self.orientation = self.decoder.get_image_orientation()
        self.magnification = self.decoder.get_image_magnification()
        self.feedback.send_comment("Ending receiving information")
