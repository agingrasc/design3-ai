from domain.command.visionregulation import VisionRegulation
from domain.gameboard.position import Position
from domain.robot.blackboard import Blackboard
from domain.robot.task.identifyantennatask.identifyantennatask import IdentifyAntennaTask
from service.globalinformation import GlobalInformation


class IdentifyAntennaTaskProxy():
    def __init__(self, identify_antenna_task: IdentifyAntennaTask, blackboard: Blackboard,
                 vision_ragulation: VisionRegulation, global_information: GlobalInformation):
        self.identify_antenna_task = identify_antenna_task
        self.blackboard = blackboard
        self.vision_regulation = vision_ragulation
        self.global_information = global_information

    def execute(self):
        if self.blackboard.has_antenna_position():
            self.global_information.send_path([self.global_information.get_robot_position(), self.blackboard.antenna_position])
            self.vision_regulation.oriente_robot(self.blackboard.antenna_position.theta)
            self.vision_regulation.go_to_position(self.blackboard.antenna_position)
        else:
            self.identify_antenna_task.execute()
