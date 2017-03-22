from enum import Enum

from mcu.robotcontroller import RobotController

NORTH = "Nord"
SOUTH = "Sud"
EAST = "Est"
WEST = "West"

FOUR = 4
TWO = 2

class Decoder:

    def __init__(self, robot_controller: RobotController):
        self.robot_controler = robot_controller
        self.result = -1
        self.image_number = 0
        self.image_orientation = NORTH
        self.image_magnification = TWO

    def decode_information(self):
        pass

    def get_image_number(self)  -> int:
        return self.image_number

    def get_image_orientation(self)  -> str:
        return self.image_orientation

    def get_image_magnification(self)  -> int:
        return self.image_magnification


class OrientationsEnum(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

class MagnificationsEnum(Enum):
    TWO = 0
    FOUR = 1