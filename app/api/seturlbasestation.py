from flask import Blueprint, request, make_response, jsonify

from domain.robot.task.taskfactory import task_factory

set_url = Blueprint('set-url', __name__)


@set_url.route('/set-url', methods=['POST'])
def set_url_():
    data = request.json
    url = data['data']['base_station_url']
    print("Setting url: {}".format(url))

    task_factory.global_information.set_url(url)
    send_response = make_response(jsonify(), 200)
    return send_response
