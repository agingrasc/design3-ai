from flask import Blueprint, request, make_response, jsonify

from domain.gameboard.position import Position
from domain.robot.task.taskfactory import task_factory
from api.gotoposition.dimensionassembler import DimensionAssembler
from api.gotoposition.positionassembler import PositionAssembler
from api.gotoposition.obstaclesassembler import ObstacleAssembler

go_to_position = Blueprint('go-to-position', __name__)

SCALING = 10
ROBOT_RADIUS = 130
OBSTACLE_PADDING = ROBOT_RADIUS / 4

dimension_assembler = DimensionAssembler(SCALING)
position_assembler = PositionAssembler(SCALING)
obstacle_assembler = ObstacleAssembler(position_assembler, dimension_assembler)


@go_to_position.route('/go-to-position', methods=['POST'])
def go_to_position_():
    print("go-to-position")
    try:
        req_info = request.json
    except Exception as e:
        print(e.with_traceback())
        return make_response(jsonify(), 400)

    destination_x = int(float(req_info['destination']['x']))
    destination_y = int(float(req_info['destination']['y']))
    destination_t = float(req_info['destination']['theta'])

    destination = Position(destination_x, destination_y, destination_t)
    print("Destination: {}\n".format(destination))
    task_factory.vision_regulation.go_to_position(destination)

    return make_response(
        jsonify({
            'x': destination_x,
            'y': destination_y,
            'theta': destination_t
        }), 200)

