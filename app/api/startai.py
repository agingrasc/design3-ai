from flask import Blueprint, request, make_response, jsonify

from domain.robot.robotai import RobotAi
from domain.robot.task.taskfactory import TaskFactory

start_ai = Blueprint('start-ai', __name__)

@start_ai.route('/start-ai', methods=['POST'])
def start_ai_():
    print("starting the ai")
    try:
        req_info = request.json
    except Exception as e:
        print(e.with_traceback())
        return make_response(jsonify(), 400)
    task_id = req_info["task_id"]

    ai = RobotAi(_decide_task_list(task_id))
    ai.execute()

    send_response = make_response(jsonify(), 200)
    return send_response


def _decide_task_list(task_id):
    tasks = {0: "COMPETITION", 1:"INITIAL_ORIENTATION", 2: "IDENTIFY_ANTENNA", 3: "RECEIVE_INFORMATION", 4: "GO_TO_IMAGE", 5: "TAKE_PICTURE"
        , 6: "GO_TO_DRAWZONE", 7: "DRAW", 8: "GO_OUT_OF_DRAWZONE", 9: "LIGHT_RED_LED"}
    task_factory = TaskFactory()
    task_execute_list = []
    if(tasks[task_id] == "COMPETITION"):
        task_execute_list = task_factory.create_competition_tasks()
    if (tasks[task_id] == "INITIAL_ORIENTATION"):
        task_execute_list = task_factory.create_initial_orientation_task()
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