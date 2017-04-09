from domain.command.visionregulation import VisionRegulation
from domain.gameboard.position import Position
from domain.robot.blackboard import Blackboard
from domain.robot.task.identifyantennatask.identifyantennatask import IdentifyAntennaTask
from service.globalinformation import GlobalInformation


class IdentifyAntennaTaskProxy():
    def __init__(self, identify_antenna_task: IdentifyAntennaTask, blackboard: Blackboard,
                 vision_ragulation: VisionRegulation, global_information: GlobalInformation, pathfinder_service):
        self.identify_antenna_task = identify_antenna_task
        self.blackboard = blackboard
        self.vision_regulation = vision_ragulation
        self.global_information = global_information
        self.pathfinder_service = pathfinder_service

    def execute(self):
        if self.blackboard.has_antenna_position():
            path = self.pathfinder_service.find(self.global_information, self.blackboard.get_antenna_position())
            self.vision_regulation.go_to_positions(path)
        else:
            self.identify_antenna_task.execute()
