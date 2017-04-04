from threading import Thread

from flask import Blueprint, request, make_response, jsonify

from domain.gameboard.position import Position
from api.gotoposition.dimensionassembler import DimensionAssembler
from api.gotoposition.positionassembler import PositionAssembler
from api.gotoposition.obstaclesassembler import ObstacleAssembler
from domain.robot.task.taskfactory import TaskFactory
from service import pathfinding_application_service

goto_pathfinder = Blueprint('goto-pathfinder', __name__)


@goto_pathfinder.route('/go-to-pathfinder', methods=['POST'])
def go_to_position_():
    print("go-to-pathfinder")
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

    Thread(target=__goto_pathfinder_run, args=[destination]).start()

    return make_response(
        jsonify({
            'x': destination_x,
            'y': destination_y,
            'theta': destination_t
        }), 200)


def __goto_pathfinder_run(destination):
    task_factory = TaskFactory()
    path = pathfinding_application_service.find(task_factory.global_information, destination)
    task_factory.vision_regulation.go_to_positions(path)
