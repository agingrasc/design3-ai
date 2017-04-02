"""" Module contenant les commandes valident que l'IA peut envoyer au robot. """
from abc import ABCMeta, abstractmethod

from mcu.regulator import DEFAULT_DELTA_T, regulator
from . import protocol
from .protocol import Leds




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
