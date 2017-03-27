from flask import Blueprint, request, make_response, jsonify
from threading import Thread

from domain.robot.robotai import RobotAi
from domain.robot.task.taskfactory import task_factory

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
    Thread(target=ai.execute).start()

    send_response = make_response(jsonify(), 200)
    return send_response


def _decide_task_list(task_id):
    task_id = int(task_id)
    tasks = {0: task_factory.create_competition_tasks,
             1: task_factory.create_initial_orientation_task,
             2: task_factory.create_indentify_antenna_task,
             3: task_factory.create_receive_informations_task,
             4: task_factory.create_go_to_image_task,
             5: task_factory.create_take_picture_task,
             6: task_factory.create_go_to_drawzone_task,
             7: task_factory.create_draw_task,
             8: task_factory.create_go_out_of_drawzone_task,
             9: task_factory.create_light_red_led_task,
             10: task_factory.create_pololu_task}

    task_execute_list = tasks[task_id]()

    return task_execute_list
