from domain.gameboard.position import Position
from domain.pathfinding.pathfinding import NoPathFound
from service.globalinformation import GlobalInformation
from domain.robot.blackboard import POSITIONS

STOP_POSITION_LIST = [Position(1250, 580, 0), Position(1250, 880, 0), Position(1250, 380, 0), Position(1250, 20,
                                                                                                       0)]  # 1280, 865


class SafeZoneFinder:
    def __init__(self, pathfinding_application_service, global_information: GlobalInformation):
        self.pathfinder_service = pathfinding_application_service
        self.global_information = global_information
        self.list_path = []

    def find_safe_zone(self, positions=STOP_POSITION_LIST):
        for position in positions:
            try:
                path = self.pathfinder_service.find(self.global_information, position)
                if not len(path) == 0 and path[len(path) - 1] == position:
                    self.list_path.append(path)
            except NoPathFound:
                pass

        if len(self.list_path) == 0:
            print("Find safer zone")
            return self.find_safe_zone(POSITIONS)

        path_to_return = self.list_path[0]
        for path_found in self.list_path:
            if (len(path_found) < len(path_to_return)):
                path_to_return = path

        return path_to_return
