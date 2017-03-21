from flask import Blueprint, request, make_response, jsonify
from service import pathfinding_application_service
from domain.gameboard.position import Position
from domain.pathfinding import get_segments
from domain.command.commandcontroller import CommandController
from mcu import robotcontroller

from domain.gameboard.position import Position
from mcu.robotcontroller import robot_controller
from mcu.commands import regulator, MoveCommand
from mcu import protocol
from domain.command.visionregulation import vision_regulator

from domain.pathfinding import get_segments

go_to_position = Blueprint('go-to-position', __name__)

commandcontroller = CommandController(robotcontroller.robot_controller)
SCALING = 10


@go_to_position.route('/go-to-position', methods=['POST'])
def go_to_position_():
    print("go-to-position")
    try:
        req_info = request.json
    except Exception as e:
        print(e.with_traceback())
        return make_response(jsonify(), 400)
    robot = req_info["robot"]
    robot_pos = robot['position']
    theta = robot_pos['theta']

    destination = req_info["destination"]
    destination_x = int(float(destination["x"]) / SCALING)
    destination_y = int(float(destination["y"]) / SCALING)
    destination_t = float(destination['theta'])
    destination_position = Position(destination_x, destination_y,
                                    destination_t)

    robot_pos_x = int(float(robot_pos["x"]) / SCALING)
    robot_pos_y = int(float(robot_pos["y"]) / SCALING)
    robot_position = Position(robot_pos_x, robot_pos_y)

    base_tabel = req_info["base_table"]
    width = int(float(base_tabel["dimension"]["width"]) / SCALING)
    lenght = int(float(base_tabel["dimension"]["lenght"]) / SCALING)

    path = pathfinding_application_service.find(
        [], width, lenght, robot_position, destination_position)
    path = get_segments(path)
    upscale_path = []
    for p in path:
        upscale_path.append(Position(p.pos_x * SCALING, p.pos_y * SCALING))

    vision_regulator.push_path(upscale_path)

    vision_regulator.go_to_positions(upscale_path)

    return make_response(
        jsonify({
            'x': destination_x,
            'y': destination_y
        }), 200)
