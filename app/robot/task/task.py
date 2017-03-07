from mcu.robotcontroller import RobotController

class task():
    def __init__(self):
        self.robot_controller = RobotController()
        self.id_image = 0
        self.magnification = 0
        self.orientation = "north"

    def execute(self):
        pass