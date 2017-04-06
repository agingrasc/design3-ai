from flask import Blueprint, request, make_response, jsonify
from threading import Thread

def create_start_ai_blueprint(task_factory, robot_ai):
    start_ai_blueprint = Blueprint('start-ai', __name__)

    @start_ai_blueprint.route('/start-ai', methods=['POST'])
    def start_ai_():
        try:
            req_info = request.json
        except Exception as e:
            print(e.with_traceback())
            return make_response(jsonify(), 400)

        task_id = req_info["task_id"]

        tasks = _decide_task_list(task_id)

        ai_execution_thread = Thread(target=robot_ai.execute, args=[tasks])
        ai_execution_thread.start()

        send_response = make_response(jsonify(), 200)
        return send_response

    def _decide_task_list(task_id):
        task_id = int(task_id)

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

        if task_id == 0:
            return tasks[task_id]()
        else:
            return [tasks[task_id]()]

    return start_ai_blueprint
