import requests as req
from flask import Blueprint, request, make_response, jsonify

from domain.robot.task.taskfactory import TaskFactory


BASE_STATION_API_URL = "http://{}:12345/feedback-task"

send_feedback = Blueprint('send-feedback', __name__)


@send_feedback.route('/send-feedback', methods=['POST'])
def send_feedback_():
    data = request.json

    print(data["feedback"])

    task_factory = TaskFactory()
    url = task_factory.global_information.base_station_url
    req.post(url=BASE_STATION_API_URL.format(url), json=data)
    send_response = make_response(jsonify(), 200)
    return send_response
