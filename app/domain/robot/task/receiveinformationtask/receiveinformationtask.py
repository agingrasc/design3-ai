from domain.command.decoder import Decoder
from domain.command.visionregulation import VisionRegulation
from domain.robot.blackboard import Blackboard
from domain.robot.task.task import Task
from service.feedback import Feedback
from service.globalinformation import GlobalInformation
from service.feedback import TASK_RECEIVE_INFORMATION

class ReceiveInformationTask(Task):
    def __init__(self, feedback: Feedback, decoder: Decoder, vision_regulation: VisionRegulation, blackboard: Blackboard
                 , global_information: GlobalInformation):
        self.feedback = feedback
        self.decoder = decoder
        self.vision_regulation = vision_regulation
        self.blackboard = blackboard
        self.global_information = global_information

    def execute(self):
        antenna_pos = self.blackboard.antenna_position
        self.global_information.send_path([self.global_information.get_robot_position(), antenna_pos])
        self.vision_regulation.go_to_position(antenna_pos)
        self.decoder.decode_information()
        self.blackboard.id_image = self.decoder.get_image_number()
        self.blackboard.orientation = self.decoder.get_image_orientation()
        self.blackboard.magnification = self.decoder.get_image_magnification()
        self.feedback.send_comment(TASK_RECEIVE_INFORMATION)
