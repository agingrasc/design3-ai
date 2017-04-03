import requests as req
from flask import Blueprint, request, make_response, jsonify

from domain.robot.task.taskfactory import TaskFactory


light_green_led = Blueprint('light-green-led', __name__)


@light_green_led.route('/light-green-led', methods=['POST'])
def light_green_led_():
    task_factory = TaskFactory()
    task_factory.lighter.light_green_led_for_picture()
    send_response = make_response(jsonify(), 200)
    return send_response