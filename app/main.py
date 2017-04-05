import sys
import requests

from flask import Flask, jsonify, make_response, request

from api.setimagesegments import set_image_segments
from api.gotopathfinder import goto_pathfinder
from api.sendfeedbacktask import send_feedback
from api.lightgreenled import light_green_led
from api.seturlbasestation import set_url
from api.startai import create_start_ai_blueprint
from api.gotoposition.gotoposition import create_go_to_position_blueprint

from domain.robot.task.taskfactory import TaskFactory
from mcu.robotcontroller import RobotController
from mcu.regulator import regulator, constants, PIDConstants
from service.globalinformation import GlobalInformation


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

    global_information = GlobalInformation()

    robot_controller = RobotController(global_information, regulator)
    task_factory = TaskFactory(global_information, robot_controller)

    start_ai = create_start_ai_blueprint(task_factory)
    go_to_position = create_go_to_position_blueprint(task_factory)

    app = create_rest_api(start_ai, send_feedback, set_image_segments,
                          light_green_led, set_url, go_to_position, goto_pathfinder)

    @app.route("/regulator/constants", methods=["GET"])
    def get_regulator_constants():
        return make_response(jsonify(regulator.get_constants()))

    @app.route("/regulator/constants", methods=["POST"])
    def set_regulator_constants():
        data = request.json

        new_constants = PIDConstants(
            data['kp'],
            data['ki'],
            data['kd'],
            data['theta_kp'],
            data['theta_ki'],
            data['position_deadzone'],
            data['max_cmd'],
            data['deadzone_cmd'],
            data['min_cmd'],
            data['theta_max_cmd'],
            data['theta_min_cmd']
        )

        regulator.set_constants(new_constants)

        return make_response(jsonify({"message": "constant change", "data": regulator.get_constants()}))

    if status == AUTOMATIC:
        print("AUTOMATIC MODE not implemented")
    elif status == MANUAL:
        print("MANUAL MODE")
    else:
        print("Bad arguments : manual or automatic")

    app.run(host='0.0.0.0', port=5000)


if __name__ == '__main__':
    main()
