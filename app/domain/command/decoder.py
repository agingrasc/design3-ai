from mcu.protocol import ManchesterResultCode

from mcu.robotcontroller import RobotController

NORTH = "NORTH"
SOUTH = "SOUTH"
EAST = "EAST"
WEST = "WEST"

SCALING_FACTOR_FOUR = 4
SCALING_FACTOR_TWO = 2

ORIENTATION = {0: NORTH, 1: EAST, 2: SOUTH, 3: WEST}
MAGNIFICATION = {0: SCALING_FACTOR_TWO, 1: SCALING_FACTOR_FOUR}


class Decoder:
    def __init__(self, robot_controller: RobotController):
        self.robot_controller = robot_controller
        self.result = -1
        self.image_number = 0
        self.image_orientation = NORTH
        self.image_magnification = SCALING_FACTOR_TWO

    def decode_information(self):
        while self.result != ManchesterResultCode.SUCCESS.value:
            decoded_information = self.robot_controller.decode_manchester()
            self.result, self.image_number, self.image_orientation, self.image_magnification = decoded_information

            self.image_orientation = ORIENTATION[self.image_orientation]
            self.image_magnification = MAGNIFICATION[self.image_magnification]

    def get_image_number(self) -> int:
        return self.image_number

    def get_image_orientation(self) -> str:
        return self.image_orientation

    def get_image_magnification(self) -> int:
        return self.image_magnification
