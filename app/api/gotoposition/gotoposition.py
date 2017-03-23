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
from api.gotoposition.gotopositionAssembler import GoToPositionAssembler

from domain.pathfinding import get_segments

go_to_position = Blueprint('go-to-position', __name__)

commandcontroller = CommandController(robotcontroller.robot_controller)
SCALING = 10
ROBOT_RADIUS = 100
OBSTACLE_PADDING = ROBOT_RADIUS / 4

go_to_positiont_assembler = GoToPositionAssembler(SCALING)


@go_to_position.route('/go-to-position', methods=['POST'])
def go_to_position_():
    print("go-to-position")
    try:
        req_info = request.json
    except Exception as e:
        print(e.with_traceback())
        return make_response(jsonify(), 400)
    obstacles = req_info['obstacles']

    destination = req_info["destination"]
    destination_position = go_to_positiont_assembler.convert_position_from_json(
        destination)

    robot = req_info["robot"]["position"]
    robot_position = go_to_positiont_assembler.convert_position_from_json(
        robot)

    world_dimension = go_to_positiont_assembler.convert_dimension_from_json(
        req_info)
    width = world_dimension[0]
    lenght = world_dimension[1]

    obj_obstacles = []
    for obs_json in obstacles:
        x = int(float(obs_json['position']['x']) / SCALING)
        y = int(float(obs_json['position']['y']) / SCALING)
        radius = int(float(obs_json['dimension']['width']) / (SCALING / 2))
        radius = 5
        if obs_json['tag'] == "LEFT":
            tag = Tag.CANT_PASS_LEFT
        elif obs_json['tag'] == "RIGHT":
            tag = Tag.CANT_PASS_RIGHT
        else:
            tag = ""
        obs = ObstacleValueObject(x, y, radius, tag)
        obj_obstacles.append(obs)

    path = pathfinding_application_service.find(
        obj_obstacles, width, lenght, robot_position, destination_position,
        int(ROBOT_RADIUS / SCALING))
    path = get_segments.get_filter_path(path)
    upscale_path = []
    for p in path:
        upscale_path.append(
            Position(p.pos_x * SCALING, p.pos_y * SCALING, destination_t))

    vision_regulator.push_path(upscale_path)

    vision_regulator.go_to_positions(upscale_path)

    return make_response(
        jsonify({
            'x': destination_x,
            'y': destination_y
        }), 200)
