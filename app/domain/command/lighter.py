from mcu.robotcontroller import RobotController


class Lighter:
    def __init__(self, robot_controller: RobotController):
        self.robot_controller = robot_controller

    def light_red_led(self):
        self.robot_controller.light_red_led()

    def shut_down_red_led(self):
        self.robot_controller.shutdown_red_led()

    def light_green_led_for_picture(self):
        self.robot_controller.blink_green_led()
