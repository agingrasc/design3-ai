import sys
import requests

from flask import Flask, jsonify, make_response

from api.setimagesegments import set_image_segments
from api.gotopathfinder import goto_pathfinder
from api.sendfeedbacktask import send_feedback
from api.lightgreenled import light_green_led
from api.seturlbasestation import set_url
from api.startai import create_start_ai_blueprint
from api.gotoposition.gotoposition import go_to_position

from domain.robot.task.taskfactory import TaskFactory


def create_rest_api(start_ai, send_feedback, set_image_segments, light_green_led, set_url, go_to_position,
                    goto_pathfinder):
    app = Flask(__name__)

    @app.after_request
    def after_request(data):
        response = make_response(data)
        response.headers['Content-Type'] = 'application/json'
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers[
            'Access-Control-Allow-Headers'] = "Origin, X-Requested-With, Content-Type, Accept"
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE'
        return response

    @app.route('/take-picture', methods=['POST'])
    def take_picture():
        robot_response = requests.post('http://127.0.0.1:4000/take-picture').json()
        return make_response(jsonify(robot_response))

    @app.errorhandler(404)
    def not_found(error):
        return make_response(jsonify({'error': 'Not Found'}), 404)

    @app.route('/hello', methods=["GET"])
    def get_hello():
        return make_response(jsonify({"message": "hello"}))

    app.register_blueprint(start_ai)
    app.register_blueprint(send_feedback)
    app.register_blueprint(set_image_segments)
    app.register_blueprint(light_green_led)
    app.register_blueprint(set_url)
    app.register_blueprint(go_to_position)
    app.register_blueprint(goto_pathfinder)

    return app


def main():
    status = sys.argv[1]

    MANUAL = "manual"
    AUTOMATIC = "automatic"

    # FIXME: create instance and inject it
    task_factory = TaskFactory()

    start_ai = create_start_ai_blueprint(task_factory)

    app = create_rest_api(start_ai, send_feedback, set_image_segments,
                          light_green_led, set_url, go_to_position, goto_pathfinder)

    if status == AUTOMATIC:
        print("AUTOMATIC MODE not implemented")
    elif status == MANUAL:
        print("MANUAL MODE")
    else:
        print("Bad arguments : manual or automatic")

    app.run(host='0.0.0.0', port=6000)


if __name__ == '__main__':
    main()
