from flask import Blueprint, request, make_response, jsonify

end_light_red_led_task = Blueprint('end-light-red-led-task', __name__)

@end_light_red_led_task.route('/end-light-red-led-task', methods=['POST'])
def end_light_red_led_task_():
    print("sending end message of lighting the red led to the base station")

    send_response = make_response(jsonify(), 200)
    return send_response