import requests as req
from flask import Blueprint, request, make_response, jsonify

from api.sendfeedbacktask import BASE_STATION_API_URL
from domain.robot.task.taskfactory import task_factory

set_url = Blueprint('set-url', __name__)


@set_url.route('/set-url', methods=['POST'])
def set_url_():
    data = request.json
    #here
    print(data["feedback"])

    url = task_factory.global_information.base_station_url
    req.post(url=BASE_STATION_API_URL.format(url), json=data)
    send_response = make_response(jsonify(), 200)
    return send_response