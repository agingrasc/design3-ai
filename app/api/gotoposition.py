from flask import Blueprint, request, make_response, jsonify

from mcu.robotcontroller import RobotController
import mcu.protocol as protocol

go_to_position = Blueprint('go-to-position', __name__)

robot = RobotController()
robot.startup_test()

@go_to_position.route('/go-to-position', methods=['POST'])
def go_to_position_():
    print("go-to-position")
    pos_x = request.json["x"]
    pos_y = request.json["y"]

    if abs(pos_x) > 100:
        pos_x = 0
    if abs(pos_y) > 100:
        pos_y = 0

    dir_x = protocol.MotorsDirection.FORWARD
    dir_y = protocol.MotorsDirection.FORWARD

    if pos_x < 0:
        dir_x = protocol.MotorsDirection.BACKWARD

    if pos_y <0 :
        dir_y = protocol.MotorsDirection.BACKWARD

    robot.ser.write(protocol.generate_manual_speed_command(protocol.Motors.FRONT_X), abs(pos_x), dir_x)
    robot.ser.write(protocol.generate_manual_speed_command(protocol.Motors.REAR_X), abs(pos_x), dir_x)
    robot.ser.write(protocol.generate_manual_speed_command(protocol.Motors.FRONT_Y), abs(pos_y), dir_y)
    robot.ser.write(protocol.generate_manual_speed_command(protocol.Motors.REAR_Y), abs(pos_y), dir_y)

    return make_response(jsonify({'x': pos_x, 'y': pos_y}), 200)
