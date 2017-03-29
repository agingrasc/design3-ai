from threading import Thread

from flask import Blueprint, request, make_response, jsonify

from domain.robot.task.taskfactory import task_factory

set_image_segments = Blueprint('set-image-segments', __name__)


@set_image_segments.route('/set-image-segments', methods=['POST'])
def set_image_segments_():
    print("go-to-pathfinder")
    try:
        req_info = request.json
    except Exception as e:
        print(e.with_traceback())
        return make_response(jsonify(), 400)

    segments = req_info['data']['segments']
    task_factory.blackboard.segments_image = segments

    return make_response(
        jsonify({}), 200)

