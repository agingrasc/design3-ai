from flask import Blueprint, request, make_response, jsonify

end_identify_antenna_task = Blueprint('end-identify-antenna-task', __name__)

@end_identify_antenna_task.route('/end-identify-antenna-task', methods=['POST'])
def end_identify_antenna_task_():
    print("sending end message of identify antenna to base station")

    send_response = make_response(jsonify(), 200)
    return send_response