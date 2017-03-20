from flask import Blueprint, request, make_response, jsonify

end_receive_information_task = Blueprint('end-receive-information-task', __name__)

@end_receive_information_task.route('/end-receive-information-task', methods=['POST'])
def end_receive_information_task_():
    print("sending end message of receiving the information to base station")

    send_response = make_response(jsonify(), 200)
    return send_response