import sys
from flask import Flask, jsonify, make_response

# from api import ledok
from api.gotoposition import go_to_position
# from mcu.robotcontroller import RobotController, robot_controller
from robot.robotai import robot_ai

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


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not Found'}), 404)


if __name__ == '__main__':
    status = sys.argv[1]
    if status == AUTOMATIC:
        print("AUTOMATIC MODE not implemented")
    elif status == MANUAL:
        print("MANUAL MODE")
        # robot_controller.startup_test()
        app.register_blueprint(go_to_position)
        # app.register_blueprint(ledok.led_ok)
        ai = robot_ai()
        ai.start(7)


    else:
        print("Bad arguments : manual or automatic")
    app.run(host='0.0.0.0')
