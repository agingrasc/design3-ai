from flask import Blueprint, request, make_response, jsonify

end_go_to_image_task = Blueprint('end-go-to-image-task', __name__)

@end_go_to_image_task.route('/end-go-to-image-task', methods=['POST'])
def end_go_to_image_task_():
    print("sending end message of going to the image to the base station")

    send_response = make_response(jsonify(), 200)
    return send_response