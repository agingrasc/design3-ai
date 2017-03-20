from flask import Blueprint, request, make_response, jsonify

end_take_picture_task = Blueprint('end-take-picture-task', __name__)

@end_take_picture_task.route('/end-take-picture-task', methods=['POST'])
def end_take_picture_task_():
    print("sending end message of taking the picture to the base station")

    send_response = make_response(jsonify(), 200)
    return send_response