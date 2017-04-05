import math
from collections import namedtuple

import numpy as np
from typing import List, Tuple

from domain.gameboard.position import Position

# 2Pi rad en 10,66 secondes (0.5) et 17,25 secondes (0.3)
PIDConstants = namedtuple("PIDConstants",
                          'kp ki kd theta_kp theta_ki position_deadzone max_cmd deadzone_cmd min_cmd theta_max_cmd theta_min_cmd')

DEADZONE = 2  # mm
THETA_DEADZONE = 0.044 # rad
DEFAULT_DELTA_T = 0.100  # en secondes
MAX_X = 200
MAX_Y = 100
POSITION_ACC_DECAY = 1.00  # 3 iteration pour diminuer de moitie
THETA_ACC_DECAY = 0.79
DEFAULT_KP = 0.4
DEFAULT_KI = 0
DEFAULT_KD = 0
DEFAULT_THETA_KP = 0.50
DEFAULT_THETA_KI = 0.007
DEFAULT_MAX_CMD = 150
DEFAULT_MIN_CMD = 3
DEFAULT_THETA_MAX_CMD = 0.8
DEFAULT_THETA_MIN_CMD = 0.050

DEFAULT_DEADZONE_CMD = 0


class PIPositionRegulator(object):
    """ Implémente un régulateur PI qui agit avec une rétroaction en position et génère une commande de vitesse."""

    def __init__(self, kp=DEFAULT_KP, ki=DEFAULT_KI, kd=DEFAULT_KD, theta_kp=DEFAULT_THETA_KP,
                 theta_ki=DEFAULT_THETA_KI, position_deadzone=DEADZONE, max_cmd=DEFAULT_MAX_CMD,
                 deadzone_cmd=DEFAULT_DEADZONE_CMD, min_cmd=DEFAULT_MIN_CMD, theta_max=DEFAULT_THETA_MAX_CMD,
                 theta_min=DEFAULT_THETA_MIN_CMD):
        self._setpoint: Position = Position()
        self.accumulator = [0, 0, 0]
        self.constants = PIDConstants(kp, ki, kd, theta_kp, theta_ki, position_deadzone, max_cmd, deadzone_cmd, min_cmd, theta_max,
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
                                      theta_kp,
                                      theta_ki,
                                      deadzone,
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

        err_vec = Position(err_x, err_y)
        # dynamic_speed_x = abs(math.cos(err_vec.get_angle()) * self.constants.max_cmd)
        # dynamic_speed_y = abs(math.sin(err_vec.get_angle()) * self.constants.max_cmd)

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
        cmd_x, cmd_y = correct_for_referential_frame(cmd_x, cmd_y, actual_theta)

        # correction referentiel
        corrected_err_x, corrected_err_y = correct_for_referential_frame(err_x, err_y, actual_theta)

        # saturation de la commande x/y
        # dynamic_speeds = [dynamic_speed_x, dynamic_speed_y, self.constants.theta_max_cmd]
        # dynamic_speeds = [dynamic_speed_x, dynamic_speed_y, self.constants.theta_max_cmd]
        dynamic_speeds = [self.constants.max_cmd, self.constants.max_cmd, self.constants.theta_max_cmd]
        saturated_cmd = []
        for idx, cmd in enumerate([cmd_x, cmd_y]):
            saturated_cmd.append(self._saturate_cmd(cmd, dynamic_speeds[idx]))

        # deadzone pour arret du mouvement
        if abs(corrected_err_x) < self.constants.position_deadzone:
            saturated_cmd[0] = 0
            self.accumulator[0] = 0
        if abs(corrected_err_y) < self.constants.position_deadzone:
            saturated_cmd[1] = 0
            self.accumulator[1] = 0

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

        print("Acc: {} -- {} -- {}".format(self.accumulator[0], self.accumulator[1], self.accumulator[2]))
        print("Distance ({}): {} -- {}".format(math.sqrt(err_x**2 + err_y**2), err_x, err_y))

        command = []
        for cmd in saturated_cmd:
            command.append(int(cmd))
        command.append(saturated_theta)
        print("Commandes: {} -- {} -- {}".format(*command))
        return command

    def _relinearize(self, cmd):
        """" Force la valeur de cmd dans [deadzone_cmd, max_cmd] ou 0 si dans [-min_cmd, min_cmd]"""
        if cmd > 0:
            return cmd + self.constants.min_cmd
        elif cmd < 0:
            return cmd - self.constants.min_cmd
        else:
            return cmd

    def _saturate_cmd(self, cmd, max_cmd):
        if cmd > max_cmd:
            return max_cmd
        elif cmd < -max_cmd:
            return -max_cmd
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
        deadzone *= 1.2
        theta_deadzone = THETA_DEADZONE * 1.03
        err_x = robot_position.pos_x - self.setpoint.pos_x
        err_y = robot_position.pos_y - self.setpoint.pos_y
        err_theta = wrap_theta(robot_position.theta - self.setpoint.theta)
        return abs(err_x) < deadzone and abs(err_y) < deadzone and abs(err_theta) < theta_deadzone


def correct_for_referential_frame(x: float, y: float, t: float) -> Tuple[float, float]:
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


# FIXME: instance statique, mettre dans RobotController
regulator = PIPositionRegulator()
