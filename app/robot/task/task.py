# from mcu.robotcontroller import RobotController

class task():
    def __init__(self, robot_controler = None):
        # if robot_controler:
        #     self.robot_controller = robot_controler
        # else:
        #     self.robot_controller = RobotController()
        self.id_image = 0
        self.magnification = 0
        self.orientation = "north"
        self.segments_image = []

    def execute(self, x_robot_position, y_robot_position):
        pass