from flask import Blueprint, request, make_response, jsonify
from app.service import pathfinding_application_service
from app.domain.gameboard.position import Position
from app.domain.pathfinding import get_segments
from app.domain.command.commandcontroller import CommandController
from app.mcu import robotcontroller

from domain.gameboard.position import Position
from mcu.robotcontroller import robot_controller
from mcu.commands import regulator, MoveCommand
from mcu import protocol

go_to_position = Blueprint('go-to-position', __name__)

commandcontroller = CommandController(robotcontroller.robot_controller)


@go_to_position.route('/go-to-position', methods=['POST'])
def go_to_position_():
    print("go-to-position")
    try:
        req_info = request.json
    except Exception as e:
        return make_response(jsonify(), 400)
    robot = req_info["robot"]
    robot_x = robot["x"]
    robot_y = robot["y"]
    theta = robot['theta']
    obstacles = req_info["obstacles"]
    width = request["width"]
    length = request["length"]
    robot_position = Position(robot_x, robot_y)
    destination = req_info["destination"]
    destination_x = destination["x"]
    destination_y = destination["y"]
    destination_position = Position(destination_x, destination_y, theta)
    path = pathfinding_application_service.find(obstacles, width, length,
                                                robot_position, destination)
    destinations = get_segments.get_filter_path(path)
    for point in destinations:
        regulator.set_point = destination_position

    return make_response(
        jsonify({
            'x': destination_x,
            'y': destination_y
        }), 200)
