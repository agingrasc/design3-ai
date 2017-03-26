import sys
from flask import Flask, jsonify, make_response
import requests

from api.sendfeedbacktask import send_feedback

from api.startai import start_ai

from api.gotoposition.gotoposition import go_to_position

from domain.robot.task.taskfactory import task_factory

app = Flask(__name__)

MANUAL = "manual"
AUTOMATIC = "automatic"


def run_automatic():
    print("run robot AI")

def run_manual():
    print("run manual")

@app.after_request
def after_request(data):
    response = make_response(data)
    response.headers['Content-Type'] = 'application/json'
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers[
        'Access-Control-Allow-Headers'] = "Origin, X-Requested-With, Content-Type, Accept"
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE'
    return response


def bad_request(error):
    return make_response(jsonify({'error': 'Bad Request'}), 400)

@app.route('/take-picture', methods=['POST'])
def take_picture():
    robot_response = requests.post('http://127.0.0.1:4000/take-picture').json()
    return make_response(jsonify(robot_response))


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not Found'}), 404)


def main():
    status = sys.argv[1]
    base_station_url = sys.argv[2]
    task_factory.set_url(base_station_url)

    app.register_blueprint(start_ai)
    app.register_blueprint(send_feedback)

    if status == AUTOMATIC:
        print("AUTOMATIC MODE not implemented")
    elif status == MANUAL:
        print("MANUAL MODE")
        app.register_blueprint(go_to_position)

    else:
        print("Bad arguments : manual or automatic")
    task_factory.global_information.get_obstacles()
    app.run(host='0.0.0.0')


if __name__ == '__main__':
    main()
