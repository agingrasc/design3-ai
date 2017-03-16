import sys
from flask import Flask, jsonify, make_response

from api import ledok
from api.gotoposition import go_to_position
from mcu.robotcontroller import RobotController, robot_controller
from robot.robotai import RobotAi
from robot.task.taskfactory import TaskFactory

app = Flask(__name__)

MANUAL = "manual"
AUTOMATIC = "automatic"

def run_automatic():
    print("run robot AI")


def run_manual():
    print("run manual")

def decide_task_list(task_id):
    tasks = {0: "COMPETITION", 1: "IDENTIFY_ANTENNA", 2: "RECEIVE_INFORMATION", 3: "GO_TO_IMAGE", 4: "TAKE_PICTURE"
        , 5: "GO_TO_DRAWZONE", 6: "DRAW", 7: "GO_OUT_OF_DRAWZONE", 8: "LIGHT_RED_LED"}
    task_factory = TaskFactory()
    task_execute_list = []
    if(tasks[task_id] == "COMPETITION"):
        task_execute_list = task_factory.create_competition_tasks()
    if (tasks[task_id] == "IDENTIFY_ANTENNA"):
        task_execute_list = task_factory.create_indentify_antenna_task()
    if (tasks[task_id] == "RECEIVE_INFORMATION"):
        task_execute_list = task_factory.create_receive_informations_task()
    if (tasks[task_id] == "GO_TO_IMAGE"):
        task_execute_list = task_factory.create_go_to_image_task()
    if (tasks[task_id] == "TAKE_PICTURE"):
        task_execute_list = task_factory.create_take_picture_task()
    if (tasks[task_id] == "GO_TO_DRAWZONE"):
        task_execute_list = task_factory.create_go_to_drawzone_task()
    if (tasks[task_id] == "DRAW"):
        task_execute_list = task_factory.create_draw_task()
    if (tasks[task_id] == "GO_OUT_OF_DRAWZONE"):
        task_execute_list = task_factory.create_go_out_of_drawzone_task()
    if (tasks[task_id] == "LIGHT_RED_LED"):
        task_execute_list = task_factory.create_light_red_led_task()

    return task_execute_list

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
    task_id = sys.argv[2]
    ai = RobotAi(decide_task_list(task_id))
    if status == AUTOMATIC:
        print("AUTOMATIC MODE not implemented")
    elif status == MANUAL:
        print("MANUAL MODE")
        app.register_blueprint(go_to_position)
        app.register_blueprint(ledok.led_ok)
        ai.execute()

    else:
        print("Bad arguments : manual or automatic")
    app.run(host='0.0.0.0')
