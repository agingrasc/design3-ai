from flask import Blueprint, request, make_response, jsonify

end_initial_orientation_task = Blueprint('end-initial-orientation-task', __name__)

@end_initial_orientation_task.route('/end-initial-orientation-task', methods=['POST'])
def end_initial_orientation_task_():
    print("sending end of initial orientation to base station")

    send_response = make_response(jsonify(), 200)
    return send_response