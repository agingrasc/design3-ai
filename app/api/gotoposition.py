from flask import Blueprint, request, make_response, jsonify
from service import pathfinding_application_service
from domain.gameboard.position import Position
from domain.pathfinding import get_segments
from domain.command.commandcontroller import CommandController
from mcu import robotcontroller

from domain.gameboard.position import Position
from domain.gameboard.gameboard import ObstacleValueObject
from domain.gameboard.gameboard import Tag
from mcu.robotcontroller import robot_controller
from mcu.commands import regulator, MoveCommand
from mcu import protocol
from domain.command.visionregulation import vision_regulator

from domain.pathfinding import get_segments

go_to_position = Blueprint('go-to-position', __name__)

commandcontroller = CommandController(robotcontroller.robot_controller)
SCALING = 10
ROBOT_RADIUS = 100
OBSTACLE_PADDING = ROBOT_RADIUS / 4


@go_to_position.route('/go-to-position', methods=['POST'])
def go_to_position_():
    print("go-to-position")
    try:
        req_info = request.json
    except Exception as e:
        print(e.with_traceback())
        return make_response(jsonify(), 400)
    robot = req_info["robot"]
    obstacles = req_info['obstacles']
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

    width = int(float(req_info["width"]) / SCALING)
    lenght = int(float(req_info["length"]) / SCALING)
    obj_obstacles = []
    for obs_json in obstacles:
        x = int(float(obs_json['position']['x']) / (SCALING * 2))
        y = int(float(obs_json['position']['y']) / (SCALING * 2))
        radius = int(float(obs_json['dimension']['width']) / SCALING)
        if obs_json['tag'] == "LEFT":
            tag = Tag.CANT_PASS_LEFT
        elif obs_json['tag'] == "RIGHT":
            tag = Tag.CANT_PASS_RIGHT
        else:
            tag = ""
        obs = ObstacleValueObject(x, y, radius, tag)
        obj_obstacles.append(obs)

    path = pathfinding_application_service.find(
        obj_obstacles, width, lenght, robot_position, destination_position, 1)
    path = get_segments.get_filter_path(path)
    upscale_path = []
    print("PATHHHHHHHHHHHHHHHHHHHHHHHH")
    for p in path:
        print(p)
        upscale_path.append(
            Position(p.pos_x * SCALING, p.pos_y * SCALING, destination_t))
    print("FIN PATHHHHHHHHHHHHHHHHHHHHHHHH")

    vision_regulator.push_path(upscale_path)

    vision_regulator.go_to_positions(upscale_path)

    return make_response(
        jsonify({
            'x': destination_x,
            'y': destination_y
        }), 200)
