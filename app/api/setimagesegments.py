from flask import Blueprint, request, make_response, jsonify

from domain.gameboard.position import Position
from domain.robot.task.taskfactory import TaskFactory

set_image_segments = Blueprint('set-image-segments', __name__)


@set_image_segments.route('/set-image-segments', methods=['POST'])
def set_image_segments_():
    try:
        req_info = request.json
    except Exception as e:
        print(e.with_traceback())

        return make_response(jsonify(), 400)

    if 'error' in req_info:
        print(req_info)

        return make_response(jsonify({"message": "trying again"}), 400)
    else:
        segments = req_info['segments']

        image_corners = []

        for point in segments:
            image_corners.append(Position(point[0], point[1]))

        task_factory = TaskFactory()
        task_factory.blackboard.segments_image = image_corners

        return make_response(jsonify({}), 200)
