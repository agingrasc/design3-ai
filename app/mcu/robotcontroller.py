"""" Interface entre le système de prise de décision et le MCU. Se charge d'envoyer les commandes. """
import enum
from typing import List

import serial
import time
import math

from domain.gameboard.position import Position
from mcu import protocol
from mcu import servos
from mcu.commands import MoveCommand, DecodeManchesterCommand, GetManchesterPowerCommand
from mcu.regulator import correct_for_referential_frame, regulator, PIPositionRegulator
from mcu.protocol import PencilStatus
from service.globalinformation import GlobalInformation

if __name__ == "__main__":
    from mcu.protocol import Leds
    from mcu.commands import ICommand, LedCommand, MoveCommand
else:
    from mcu.protocol import Leds
    from .commands import ICommand, LedCommand

SERIAL_MCU_DEV_NAME = "ttySTM32"
SERIAL_POLULU_DEV_NAME = "ttyPololu"
REGULATOR_FREQUENCY = 0.030 # secondes


class RobotSpeed(enum.Enum):
    NORMAL_SPEED = (150, 4)
    SCAN_SPEED = (70, 5)
    DRAW_SPEED = (60, 2)


# Old constants of single PID
#constants = [(0.027069, 0.040708, 0, 20),  # REAR X
#             (0.0095292, 0.029466, 0, 20),  # FRONT Y
#             (0.015431, 0.042286, 0, 20),  # FRONT X
#             (0.030357, 0.02766, 0, 20)]  # REAR Y


constants_cw = [(0.0016763, 0.0019101, 0, 20),  # REAR X (SEMI-OK)
             (0.0023951, 0.0022002, 0, 20),  # FRONT Y (SEMI-OK)
             (0.0056477, 0.0021575, 0, 20),  # FRONT X (OK)
             (0.0067589, 0.0023039, 0, 20)] # REAR Y 0.025657 0.02366

constants_ccw = [(0.0059, 0.0020158, 0, 20),  # REAR X 0.027069 0.040708 (OK)
                (0.0013096, 0.0022507, 0, 20),  # FRONT Y
                (0.0083117, 0.0025862, 0, 20),  # FRONTX (SEMI-OK)
                (0.00018672, 0.0023825, 0, 20)] # REAR Y (SEMI-OK)


class SerialMock:
    def write(self, arg, byteorder='little'):
        print("Serial mock: {} -- ".format(arg, byteorder))
        return -1

    def read(self, nbr_byte):
        print("Serial mock reading! ({})".format(nbr_byte))
        return b'\x00'

    def inWaiting(self):
        return 0


class RobotController(object):
    """" Controleur du robot, permet d'envoyer les commandes et de recevoir certaines informations du MCU."""
    def __init__(self, global_information: GlobalInformation, regulator: PIPositionRegulator):
        """" Si aucun lien serie n'est disponible, un SerialMock est instancie."""
        try:
            self.ser_mcu = serial.Serial("/dev/{}".format(SERIAL_MCU_DEV_NAME))
        except serial.serialutil.SerialException:
            print("No serial link for mcu!")
            self.ser_mcu = SerialMock()

        try:
            self.ser_polulu = serial.Serial("/dev/{}".format(SERIAL_POLULU_DEV_NAME))
        except serial.serialutil.SerialException:
            print("No serial link for polulu!")
            self.ser_polulu = SerialMock()

        self.last_timestamp = time.time()
        self._init_mcu_pid()
        self._startup_test()
        self.global_information = global_information
        self.record_power = False
        self.powers = {}

    def send_command(self, cmd: ICommand):
        """"
        Prend une commande et s'occupe de l'envoyer au MCU.
        Args:
            :cmd: La commande a envoyer
        Returns:
            None
        """
        self.ser_mcu.write(cmd.pack_command())

    def send_move_command(self, robot_position: Position, delta_t=None, pure_orientation=False):
        now = time.time()
        if delta_t:
            regulator_delta_t = delta_t
        else:
            regulator_delta_t = now - self.last_timestamp
        self.last_timestamp = now
        cmd = MoveCommand(robot_position, regulator_delta_t, pure_orientation)
        self.ser_mcu.write(cmd.pack_command())

    def send_servo_command(self, cmd):
        """"
        Prend une commande et s'occupe de l'envoyer au Pololu.
        Args:
            :cmd: La commande a envoyer
        Returns:
            None
        """
        self.ser_polulu.write(cmd)

    def lower_pencil(self):
        cmd = servos.generate_pencil_command(servos.PencilStatus.LOWERED)
        self.send_servo_command(cmd)
        init_time = time.time()
        while time.time() - init_time < 1:
            pass

    def raise_pencil(self):
        cmd = servos.generate_pencil_command(servos.PencilStatus.RAISED)
        self.send_servo_command(cmd)
        init_time = time.time()
        while time.time() - init_time < 1:
            pass

    def light_red_led(self):
        cmd = LedCommand(Leds.UP_RED)
        self.send_command(cmd)

    def shutdown_red_led(self):
        self.reset_state()

        cmd = LedCommand(Leds.DOWN_RED)
        self.send_command(cmd)

    def blink_green_led(self):
        cmd = LedCommand(Leds.BLINK_GREEN)
        self.send_command(cmd)

    def decode_manchester(self):
        cmd = DecodeManchesterCommand()
        self.ser_mcu.read(self.ser_mcu.inWaiting())
        self.send_command(cmd)

        result_code = int.from_bytes(self.ser_mcu.read(1), byteorder='big') # Decode result (success or error)
        figure_number = int.from_bytes(self.ser_mcu.read(1), byteorder='big')
        orientation = int.from_bytes(self.ser_mcu.read(1), byteorder='big')
        scaling_factor = int.from_bytes(self.ser_mcu.read(1), byteorder='big')

        return [result_code, figure_number, orientation, scaling_factor]

    def reset_state(self):
        cmd = protocol.generate_reset_state_command()
        self.ser_mcu.read(self.ser_mcu.inWaiting())
        self.ser_mcu.write(cmd)

    def reset_traveled_distance(self):
        cmd = protocol.generate_reset_traveled_distance_command()
        self.ser_mcu.read(self.ser_mcu.inWaiting())
        self.ser_mcu.write(cmd)

    def get_traveled_distance(self):
        cmd = protocol.generate_get_traveled_distance_command()
        self.ser_mcu.read(self.ser_mcu.inWaiting())
        self.ser_mcu.write(cmd)

        traveled_distance_frontx = int.from_bytes(self.ser_mcu.read(2), byteorder='big', signed=True)
        traveled_distance_rearx = int.from_bytes(self.ser_mcu.read(2), byteorder='big', signed=True)
        traveled_distance_fronty = int.from_bytes(self.ser_mcu.read(2), byteorder='big', signed=True)
        traveled_distance_reary = int.from_bytes(self.ser_mcu.read(2), byteorder='big', signed=True)

        return [traveled_distance_frontx, traveled_distance_rearx, traveled_distance_fronty, traveled_distance_reary]
        
    def get_manchester_power(self):
        cmd = protocol.generate_get_manchester_power()
        self.ser_mcu.read(self.ser_mcu.inWaiting())
        self.ser_mcu.write(cmd)
        power_bytes = self.ser_mcu.read(2)
        power = int.from_bytes(power_bytes, byteorder='big')
        return power

    def move(self, destination: Position, pure_orientation=False):
        """" S'occupe d'amener le robot a la bonne position. BLOQUANT! """
        regulator.setpoint = destination
        retroaction = self.global_information.get_robot_position()
        now = time.time()
        last_time = now

        while not regulator.is_arrived(retroaction, regulator.constants.position_deadzone):
            retroaction = self.global_information.get_robot_position()
            now = time.time()
            delta_t = now - last_time
            if delta_t > REGULATOR_FREQUENCY:
                last_time = now
                self.send_move_command(retroaction, delta_t, pure_orientation)
                if self.record_power:
                    power_level = self.get_manchester_power()
                    print("Power level: {}".format(power_level))
                    self.powers[retroaction] = power_level

    def precise_move(self, vec: Position, speed: Position=Position(20, 20)):
        self.reset_traveled_distance()

        retroaction = self.global_information.get_robot_position()
        angle = retroaction.theta

        distance_to_move_x, distance_to_move_y = correct_for_referential_frame(vec.pos_x, vec.pos_y, angle)
        # FIXME: dynamic speed computing
        target_speed_x, target_speed_y = speed.pos_x, speed.pos_y
        if distance_to_move_x < 0:
            target_speed_x = -speed.pos_x
        if distance_to_move_y < 0:
            target_speed_y = -speed.pos_y

        last_timestamp = time.time()

        remaining_x, remaining_y = self.get_remaining_distances(distance_to_move_x, distance_to_move_y)
        while remaining_x > 0 or remaining_y > 0:
            delta_t = time.time() - last_timestamp
            if delta_t > REGULATOR_FREQUENCY:
                last_timestamp = time.time()
                if remaining_x > 0:
                    speed_x = target_speed_x
                else:
                    speed_x = 0

                if remaining_y > 0:
                    speed_y = target_speed_y
                else:
                    speed_y = 0

                cmd = protocol.generate_move_command(speed_x, speed_y, 0)
                self.ser_mcu.write(cmd)
                self.ser_mcu.read(self.ser_mcu.inWaiting())

                remaining_x, remaining_y = self.get_remaining_distances(distance_to_move_x, distance_to_move_y)

        cmd = protocol.generate_move_command(0, 0, 0)
        self.ser_mcu.write(cmd)

    def timed_move(self, destination: Position, speed=80, robot_position=None):
        move_vec = destination - robot_position
        speed_vec = move_vec.renormalize(speed)

        time_to_move = self.compute_time_move(move_vec, speed, speed_vec)
        start_time = time.time()

        last_cmd_time = time.time()
        while time.time() - start_time < time_to_move:
            if time.time() - last_cmd_time > REGULATOR_FREQUENCY:
                speed_x, speed_y = correct_for_referential_frame(speed_vec.pos_x, speed_vec.pos_y, robot_position.theta)
                self.ser_mcu.write(protocol.generate_move_command(speed_x, speed_y, 0))

        self.ser_mcu.write(protocol.generate_move_command(0, 0, 0))
        return robot_position

    def compute_time_move(self, move_vec, speed, speed_vec):
        ACCEL_X = 135  # mm/s^2 (128)
        ACCEL_Y = 220 # 160
        acceleration_time_x = speed / ACCEL_X
        acceleration_time_y = speed / ACCEL_Y
        speed_during_acceleration = speed_vec.multiply(0.50)
        move_during_acceleration = Position(speed_during_acceleration.pos_x * acceleration_time_x,
                                            speed_during_acceleration.pos_y * acceleration_time_y)
        move_vec -= move_during_acceleration
        time_to_move = (move_vec.get_norm() / speed_vec.get_norm()) + speed / Position(ACCEL_X, ACCEL_Y).get_norm()
        return time_to_move

    def get_remaining_distances(self, target_distance_x, target_distance_y):
        distances = self.get_traveled_distance()
        distance_x = distances[3]
        distance_y = distances[1]
        remaining_x = abs(target_distance_x) - abs(distance_x)
        remaining_y = abs(target_distance_y) - abs(distance_y)
        return remaining_x, remaining_y

    def start_power_recording(self):
        self.record_power = True
        self.powers = {}

    def stop_power_recording(self):
        self.record_power = False

    def get_max_power_position(self) -> Position:
        max_level = 0
        max_pos = None
        for pos, power_level in self.powers.items():
            if power_level > max_level:
                max_level = power_level
                max_pos = pos
        return max_pos

    def set_robot_speed(self, speed: RobotSpeed):
        move_speed, deadzone = speed.value
        regulator.set_speed(move_speed, deadzone)

    def _init_mcu_pid(self):
        for motor in protocol.Motors:
            kp_cw, ki_cw, kd_cw, dz_cw = constants_cw[motor.value]
            cmd = protocol.generate_set_pid_constant_forward(motor, kp_cw, ki_cw, kd_cw, dz_cw)
            self.ser_mcu.write(cmd)

            kp_ccw, ki_ccw, kd_ccw, dz_ccw = constants_ccw[motor.value]
            cmd = protocol.generate_set_pid_constant_backward(motor, kp_ccw, ki_ccw, kd_ccw, dz_ccw)
            self.ser_mcu.write(cmd)

    def _startup_test(self):
        """ Effectue un test de base pour s'assurer que le MCU repond et met le MCU en mode de debogage."""
        print("startup test")
        cmd = LedCommand(Leds.UP_GREEN)
        self.send_command(cmd)
        time.sleep(1)
        cmd = LedCommand(Leds.DOWN_GREEN)
        self.send_command(cmd)
        cmd = LedCommand(Leds.UP_RED)
        self.send_command(cmd)
        time.sleep(1)
        cmd = LedCommand(Leds.DOWN_RED)
        self.send_command(cmd)
        self.raise_pencil()
        self.reset_state()

    def _get_return_code(self):
        return int.from_bytes(self.ser_mcu.read(1), byteorder='little')
