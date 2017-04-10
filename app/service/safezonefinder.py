from domain.gameboard.position import Position
from domain.pathfinding.pathfinding import NoPathFound
from service.globalinformation import GlobalInformation

STOP_POSITION_LIST = [Position(1250, 580, 0), Position(1250, 880, 0), Position(1250, 380, 0), Position(1250, 20, 0)]  # 1280, 865

class SafeZoneFinder():

    def __init__(self, pathfinding_application_service, global_information: GlobalInformation):
        self.pathfinder_service = pathfinding_application_service
        self.global_information = global_information
        self.list_path = []

    def find_safe_zone(self, ):
        for position in STOP_POSITION_LIST:
            try:
                path = self.pathfinder_service.find(self.global_information, position)
                self.list_path.append(path)
            except NoPathFound:
                list_error = []
                self.list_path.append(list_error)

        path_to_return = self.list_path[0]
        for path_found in self.list_path:
             if (len(path_found) > 0) & (len(path_found) < len(path_to_return)):
                 path_to_return = path

        return path_to_return

