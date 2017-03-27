from domain.command.antenna import Antenna
from domain.command.decoder import Decoder
from domain.command.visionregulation import VisionRegulation
from domain.robot.blackboard import Blackboard
from domain.robot.feedback import Feedback
from domain.robot.task.task import Task


class ReceiveInformationTask(Task):
    def __init__(self, feedback: Feedback, decoder: Decoder, vision_regulation: VisionRegulation, blackboard: Blackboard):
        self.feedback = feedback
        self.decoder = decoder
        self.vision_regulation = VisionRegulation
        self.blackboard = blackboard

    def execute(self):
        antenna_pos = self.blackboard.antenna_position
        self.vision_regulation.go_to_position(antenna_pos)
        self.decoder.decode_information()
        self.blackboard.id_image = self.decoder.get_image_number()
        self.blackboard.orientation = self.decoder.get_image_orientation()
        self.blackboard.magnification = self.decoder.get_image_magnification()
        self.feedback.send_comment("Ending receiving information")
