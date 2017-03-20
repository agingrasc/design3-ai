from flask import Blueprint, request, make_response, jsonify

end_draw_task = Blueprint('end-draw-task', __name__)

@end_draw_task.route('/end-draw-task', methods=['POST'])
def end_draw_task_():
    print("sending end message of drawing to the base station")

    send_response = make_response(jsonify(), 200)
    return send_response