from mcu.robotcontroller import RobotController


class Lighter:
    def __init__(self, robot_controler: RobotController):
        self.robot_controler = robot_controler

    def light_red_led(self):
        pass

    def shut_down_red_led(self):
        pass

    def light_green_led_for_picture(self):
        pass