from flask import Blueprint, request, make_response, jsonify
from threading import Thread

from domain.robot.robotai import RobotAi


def create_start_ai_blueprint(task_factory):
    start_ai_blueprint = Blueprint('start-ai', __name__)

    @start_ai_blueprint.route('/start-ai', methods=['POST'])
    def start_ai_():
        print("starting the ai")

        try:
            req_info = request.json
        except Exception as e:
            print(e.with_traceback())
            return make_response(jsonify(), 400)

        task_id = req_info["task_id"]

        ai = RobotAi(_decide_task_list(task_id))

        ai_thread = Thread(target=ai.execute)
        ai_thread.start()

        send_response = make_response(jsonify(), 200)
        return send_response

    def _decide_task_list(task_id):
        task_id = int(task_id)

        task_factory.task_list.clear()

        tasks = {
            0: task_factory.create_competition_tasks,
            1: task_factory.create_initial_orientation_task,
            2: task_factory.create_indentify_antenna_task,
            3: task_factory.create_receive_informations_task,
            4: task_factory.create_go_to_image_task,
            5: task_factory.create_take_picture_task,
            6: task_factory.create_go_to_drawzone_task,
            7: task_factory.create_draw_task,
            8: task_factory.create_go_out_of_drawzone_task,
            9: task_factory.create_light_red_led_task
        }

        task_execute_list = tasks[task_id]()

        return task_execute_list

    return start_ai_blueprint
