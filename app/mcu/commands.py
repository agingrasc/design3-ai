"""" Module contenant les commandes valident que l'IA peut envoyer au robot. """
from abc import abstractmethod, ABCMeta
from collections import namedtuple

import math
import time
from typing import List, Tuple

import numpy as np

from domain.gameboard.position import Position
from . import protocol
from .protocol import PencilStatus, Leds

PIDConstants = namedtuple("PIDConstants",
                          'kp ki kd theta_kp theta_ki position_deadzone max_cmd deadzone_cmd min_cmd theta_max_cmd theta_min_cmd')
DEADZONE = 10 # mm
THETA_DEADZONE = 0.009 # rad
DEFAULT_DELTA_T = 0.100  # en secondes
MAX_X = 200
MAX_Y = 100
POSITION_ACC_DECAY = 0.79 # 3 iteration pour diminuer de moitie
THETA_ACC_DECAY = 0.79

DEFAULT_KP = 1.0
DEFAULT_KI = 0.01
DEFAULT_KD = 0
DEFAULT_THETA_KP = 0.1
DEFAULT_THETA_KI = 0.3
DEFAULT_MAX_CMD = 30
DEFAULT_DEADZONE_CMD = 5
DEFAULT_MIN_CMD = 5
DEFAULT_THETA_MAX_CMD = 0.2
DEFAULT_THETA_MIN_CMD = 0.025
# 2Pi rad en 10,66 secondes (0.5) et 17,25 secondes (0.3)


class PIPositionRegulator(object):
    """ Implémente un régulateur PI qui agit avec une rétroaction en position et génère une commande de vitesse."""

    def __init__(self, kp=DEFAULT_KP, ki=DEFAULT_KI, kd=DEFAULT_KD, theta_kp=DEFAULT_THETA_KP,
                 theta_ki=DEFAULT_THETA_KI, position_deadzone=DEADZONE, max_cmd=DEFAULT_MAX_CMD,
                 deadzone_cmd=DEFAULT_DEADZONE_CMD, min_cmd=DEFAULT_MIN_CMD, theta_max=DEFAULT_THETA_MAX_CMD,
                 theta_min=DEFAULT_THETA_MIN_CMD):
        self._setpoint: Position = Position()
        self.accumulator = [0, 0, 0]
        self.constants = PIDConstants(kp, ki, kd, position_deadzone, theta_kp, theta_ki, max_cmd, deadzone_cmd, min_cmd, theta_max,
                                      theta_min)

    @property
    def setpoint(self):
        return self._setpoint

    @setpoint.setter
    def setpoint(self, new_setpoint):
        """" Assigne une consigne au regulateur. Effet de bord: reinitialise les accumulateurs. """
        if self._setpoint != new_setpoint:
            self.accumulator = [0, 0, 0]
            self._setpoint = new_setpoint

    def set_speed(self, move_speed, deadzone):
        kp = self.constants.kp
        ki = self.constants.ki
        kd = self.constants.kd
        theta_kp = self.constants.theta_kp
        theta_ki = self.constants.theta_ki
        deadzone_cmd = self.constants.deadzone_cmd
        min_cmd = self.constants.min_cmd
        theta_max = self.constants.theta_max_cmd
        theta_min = self.constants.theta_min_cmd
        self.constants = PIDConstants(kp,
                                      ki,
                                      kd,
                                      deadzone,
                                      theta_kp,
                                      theta_ki,
                                      move_speed,
                                      deadzone_cmd,
                                      min_cmd,
                                      theta_max,
                                      theta_min)

    def next_speed_command(self, actual_position: Position, delta_t: float = DEFAULT_DELTA_T) -> List[int]:
        """"
        Calcul une iteration du PID.
        Args:
            :actual_position: Retroaction de la position du robot.
            :delta_t: Temps ecoule depuis le dernier appel ou la derniere assignation de consigne en secondes.
        Returns:
            La vitesse en x, y et en theta.
        """
        actual_x = actual_position.pos_x
        actual_y = actual_position.pos_y
        actual_theta = actual_position.theta
        dest_x = self.setpoint.pos_x
        dest_y = self.setpoint.pos_y
        dest_theta = self.setpoint.theta
        err_x, err_y, err_theta = dest_x - actual_x, dest_y - actual_y, dest_theta - actual_theta
        err_theta = wrap_theta(err_theta)

        # wrap theta [-PI, PI]

        # calcul PID pour x/y
        up_x = err_x * self.constants.kp
        up_y = err_y * self.constants.kp

        ui_x = self.accumulator[0] + (self.constants.ki * err_x * delta_t)
        ui_y = self.accumulator[1] + (self.constants.ki * err_y * delta_t)

        cmd_x = up_x + ui_x
        cmd_y = up_y + ui_y

        self.accumulator[0] = ui_x
        self.accumulator[1] = ui_y

        self.accumulator[0] *= POSITION_ACC_DECAY
        self.accumulator[1] *= POSITION_ACC_DECAY

        if self.accumulator[0] > self.constants.max_cmd:
            self.accumulator[0] = self.constants.max_cmd
        elif self.accumulator[0] < -self.constants.max_cmd:
            self.accumulator[0] = -self.constants.max_cmd

        if self.accumulator[1] > self.constants.max_cmd:
            self.accumulator[1] = self.constants.max_cmd
        elif self.accumulator[1] < -self.constants.max_cmd:
            self.accumulator[1] = -self.constants.max_cmd

        cmd_x = self._relinearize(cmd_x)
        cmd_y = self._relinearize(cmd_y)
        cmd_x, cmd_y = _correct_for_referential_frame(cmd_x, cmd_y, actual_theta)

        # correction referentiel
        corrected_err_x, corrected_err_y = _correct_for_referential_frame(err_x, err_y, actual_theta)

        # saturation de la commande x/y
        saturated_cmd = []
        for cmd in [cmd_x, cmd_y]:
            saturated_cmd.append(self._saturate_cmd(cmd))

        # deadzone pour arret du mouvement
        if abs(corrected_err_x) < self.constants.position_deadzone:
            saturated_cmd[0] = 0
        if abs(corrected_err_y) < self.constants.position_deadzone:
            saturated_cmd[1] = 0

        # calcul de la vitesse angulaire
        theta_up = err_theta * self.constants.theta_kp
        theta_ui = self.accumulator[2] + self.constants.theta_ki * err_theta * delta_t
        self._update_theta_accumulator(theta_ui)
        cmd_theta = theta_up + theta_ui

        # saturation de la commande theta
        saturated_theta = self._saturate_theta_cmd(cmd_theta)

        # deadzone theta
        if abs(err_theta) < THETA_DEADZONE:
            saturated_theta = 0

        command = []
        for cmd in saturated_cmd:
            command.append(int(cmd))
        command.append(saturated_theta)
        return command

    def _relinearize(self, cmd):
        """" Force la valeur de cmd dans [deadzone_cmd, max_cmd] ou 0 si dans [-min_cmd, min_cmd]"""
        if 0 < cmd < self.constants.deadzone_cmd:
            return self.constants.deadzone_cmd
        elif -self.constants.deadzone_cmd < cmd < 0:
            return -self.constants.deadzone_cmd
        else:
            return cmd

    def _saturate_cmd(self, cmd):
        if cmd > self.constants.max_cmd:
            return self.constants.max_cmd
        elif cmd < -self.constants.max_cmd:
            return -self.constants.max_cmd
        else:
            return cmd

    def _update_theta_accumulator(self, theta_ui):
        if theta_ui > self.constants.theta_max_cmd:
            theta_ui = self.constants.theta_max_cmd
        elif theta_ui < -self.constants.theta_max_cmd:
            theta_ui = -self.constants.theta_max_cmd
        self.accumulator[2] = theta_ui
        self.accumulator[2] *= THETA_ACC_DECAY

    def _saturate_theta_cmd(self, cmd):
        if cmd > self.constants.theta_max_cmd:
            return self.constants.theta_max_cmd
        elif -self.constants.theta_min_cmd < cmd < 0:
            return cmd - self.constants.theta_min_cmd
        elif 0 < cmd < self.constants.theta_min_cmd:
            return cmd + self.constants.theta_min_cmd
        elif cmd < -self.constants.theta_max_cmd:
            return -self.constants.theta_max_cmd
        return cmd

    def is_arrived(self, robot_position: Position, deadzone=DEADZONE):
        err_x = robot_position.pos_x - self.setpoint.pos_x
        err_y = robot_position.pos_y - self.setpoint.pos_y
        err_theta = robot_position.theta - self.setpoint.theta
        return math.sqrt(err_x ** 2 + err_y ** 2) < deadzone and abs(err_theta) < THETA_DEADZONE


def _correct_for_referential_frame(x: float, y: float, t: float) -> Tuple[float, float]:
    """"
    Rotation du vecteur (x, y) dans le plan monde pour l'orienter avec l'angle t du robot.
    Args:
        :x: Composante x du vecteur, dans le plan monde
        :y: Composante y du vecteur, dans le plan monde
        :t: Orientation du robot en radians dans le plan monde
    Returns:
        Un tuple contenant les composantes x et y selon le plan du robot.
    """
    t = wrap_theta(t)
    cos = math.cos(t)
    sin = math.sin(t)

    corrected_x = (x * cos - y * sin)
    corrected_y = (y * cos + x * sin)
    return corrected_x, corrected_y


def wrap_theta(t):
    return (t + np.pi) % (2 * np.pi) - np.pi


""" Regulateur de position persistent."""
regulator = PIPositionRegulator()


class ICommand(metaclass=ABCMeta):
    def __init__(self):
        pass

    @abstractmethod
    def pack_command(self) -> bytes:
        """" Indique comment prendre les informations de l'objet et des serialiser pour l'envoyer au robot."""
        pass


class MoveCommand(ICommand):
    def __init__(self, robot_position, delta_t=DEFAULT_DELTA_T):
        """"
        Args:
            :x: Position x sur le plan monde
            :y: Position y sur le plan monde
            :theta: Orientation du robot en radians
        """
        super().__init__()
        self.robot_position = robot_position
        self.delta_t = delta_t

    def pack_command(self) -> bytes:
        regulated_command = regulator.next_speed_command(self.robot_position)
        return protocol.generate_move_command(*regulated_command)


class CameraOrientationCommand(ICommand):
    def __init__(self, x_theta, y_theta):
        """"
        Args:
            :x_theta: Orientation horizontale en radians.
            :y_theta: Orientation verticale en radians.
        """
        super().__init__()
        self.x_theta = x_theta
        self.y_theta = y_theta

    def pack_command(self) -> bytes:
        return protocol.generate_camera_command(self.x_theta, self.y_theta)


class PencilRaiseLowerCommand(ICommand):
    """" Une commande Pencil permet de controler le status du prehenseur."""

    def __init__(self, status: PencilStatus):
        super().__init__()
        self.status = status

    def pack_command(self) -> bytes:
        return protocol.generate_pencil_command(self.status)


class LedCommand(ICommand):
    def __init__(self, led: Leds):
        super().__init__()
        self.led = led

    def pack_command(self) -> bytes:
        return protocol.generate_led_command(self.led)


class DecodeManchesterCommand(ICommand):
    def __init__(self):
        super().__init__()

    def pack_command(self) -> bytes:
        return protocol.generate_decode_manchester()


class GetManchesterPowerCommand(ICommand):
    def __init__(self):
        super().__init__()

    def pack_command(self) -> bytes:
        return protocol.generate_get_manchester_power()
