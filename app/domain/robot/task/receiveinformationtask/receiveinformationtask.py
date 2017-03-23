from domain.command.antenna import Antenna
from domain.command.decoder import Decoder
from domain.command.visionregulation import VisionRegulation
from domain.robot.feedback import Feedback
from domain.robot.task.task import Task


class ReceiveInformationTask(Task):
    def __init__(self, feedback: Feedback,
                        decoder: Decoder):
        self.feedback = feedback
        self.decoder = decoder

    def execute(self):
        self.decoder.decode_information()
        self.id_image = self.decoder.get_image_number()
        self.orientation = self.decoder.get_image_orientation()
        self.magnification = self.decoder.get_image_magnification()
        self.feedback.send_comment("Ending receiving information")
