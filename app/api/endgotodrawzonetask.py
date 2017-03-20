from flask import Blueprint, request, make_response, jsonify

end_go_to_drawzone_task = Blueprint('end-go-to-drawzone-task', __name__)

@end_go_to_drawzone_task.route('/end-go-to-drawzone-task', methods=['POST'])
def end_go_to_drawzone_task_():
    print("sending end message of going to the drawzone to the base station")

    send_response = make_response(jsonify(), 200)
    return send_response