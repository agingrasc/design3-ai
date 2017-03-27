"""" Ce module contient les structures de données nécessaires pour le contrôle des servomoteurs (Pololu)."""

from enum import Enum
from .protocol import PencilStatus


class CommandType(Enum):
    SET_TARGET = 0x84
    GET_POSITION = 0x90
    SET_MULTIPLE_TARGET = 0x9F


class Channels(Enum):
    CAMERA_X = 0x0
    CAMERA_Y = 0x1
    PENCIL = 0x2


class PencilTarget(Enum):
    RAISED = 1300
    LOWERED = 1900


class MinTargets(Enum):
    CAMERA_X = 1104
    CAMERA_Y = 1104


class MaxTargets(Enum):
    CAMERA_X = 1904
    CAMERA_Y = 1600


def rad_to_camera_target(x, y):
    # Converts radian to microseconds pulse length
    xt = 509.3*x + 1500
    yt = 509.3*y + 1500

    # Cap target pulse length if converted target is outside of bounds
    if xt > MaxTargets.CAMERA_X:
        xt = MaxTargets.CAMERA_X
    elif xt < MinTargets.CAMERA_X:
        xt = MinTargets.CAMERA_X

    if yt > MaxTargets.CAMERA_Y:
        yt = MaxTargets.CAMERA_Y
    elif yt < MinTargets.CAMERA_Y:
        yt = MinTargets.CAMERA_Y

    return (xt, yt)


def generate_camera_command(x, y) -> bytes:
    xt, yt = rad_to_camera_target(x, y)

    targetx = bytes([Channels.CAMERA_X, _get_lower_bits(xt), _get_higher_bits(xt)])
    targety = bytes([Channels.CAMERA_Y, _get_lower_bits(yt), _get_higher_bits(yt)])

    header = bytes([CommandType.SET_MULTIPLE_TARGET, 2]) # two targets to set
    payload = targetx + targety

    return header + payload


def generate_pencil_command(status: PencilStatus) -> bytes:
    target = PencilTarget.RAISED
    if status == PencilStatus.LOWERED:
        target = PencilTarget.LOWERED

    header = bytes([CommandType.SET_TARGET.value, Channels.PENCIL.value])
    payload = bytes([_get_lower_bits(target), _get_higher_bits(target)])

    return header + payload


def _get_higher_bits(cmd):
    return (cmd.value * 4) >> 7 & 0x7F


def _get_lower_bits(cmd):
    return (cmd.value * 4) & 0x7F
