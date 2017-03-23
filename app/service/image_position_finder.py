from enum import Enum

from domain.gameboard.position import Position

IMAGE_1 = (Position(pos_x = 200, pos_y = 10), 90)
IMAGE_2 = (Position(pos_x = 210, pos_y = 10), 90)
IMAGE_3 = (Position(pos_x = 210, pos_y = 10), 0)
IMAGE_4 = (Position(pos_x = 210, pos_y = 15), 0)
IMAGE_5 = (Position(pos_x = 210, pos_y = 20), 0)
IMAGE_6 = (Position(pos_x = 210, pos_y = 25), 0)
IMAGE_7 = (Position(pos_x = 210, pos_y = 25), -90)
IMAGE_8 = (Position(pos_x = 200, pos_y = 25), -90)

class ImagePositionFinder:
    def getImagePosition(self, image_number):
        return ImagesPosition[image_number]


class ImagesPosition(Enum):
    IMAGE_1 = 0
    IMAGE_2 = 1
    IMAGE_3 = 2
    IMAGE_4 = 3
    IMAGE_5 = 4
    IMAGE_6 = 5
    IMAGE_7 = 6
    Image_8 = 7