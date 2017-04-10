import math
import numpy as np


class Position:
    def __init__(self, pos_x = 0, pos_y = 0, theta = 0):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.theta = theta

    def __str__(self):
        return "x: {} -- y: {} -- theta: {}".format(self.pos_x, self.pos_y, self.theta)

    def get_norm(self):
        return math.sqrt(float(self.pos_x**2) + float(self.pos_y**2))

    def get_angle(self):
        return np.arctan2(float(-self.pos_y), float(self.pos_x))

    def multiply(self, operand):
        return Position(int(self.pos_x * operand), int(self.pos_y * operand), self.theta)

    def renormalize(self, norm):
        scale_factor = norm / self.get_norm()
        return self.multiply(scale_factor)

    def __add__(self, other):
        return Position(self.pos_x + other.pos_x, self.pos_y + other.pos_y, self.theta)

    def __sub__(self, other):
        return Position(self.pos_x - other.pos_x, self.pos_y - other.pos_y, self.theta)

    def __eq__(self, other):
        return self.pos_x == other.pos_x and self.pos_y == other.pos_y and self.theta == other.theta

    def __str__(self):
        return "Position: ({}, {}, {})".format(self.pos_x, self.pos_y, self.theta)

    def __repr__(self):
        return "Position({}, {}, {})".format(self.pos_x, self.pos_y, self.theta)
