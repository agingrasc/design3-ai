import sys
from flask import Flask, jsonify, make_response

from api import ledok

from api.startai import start_ai
from api.endinitialorientationtask import end_initial_orientation_task
from api.endidentifyantennatask import end_identify_antenna_task
from api.endreceiveinformationtask import end_receive_information_task
from api.endgotoimagetask import end_go_to_image_task
from api.endtakepicturetask import end_take_picture_task
from api.endgotodrawzonetask import end_go_to_drawzone_task
from api.enddrawtask import end_draw_task
from api.endgooutofdrawzonetask import end_go_out_of_drawzone_task
from api.endlightredledtask import end_light_red_led_task
from api.gotoposition.gotoposition import go_to_position
from domain.command.visionregulation import vision_regulator

app = Flask(__name__)

MANUAL = "manual"
AUTOMATIC = "automatic"


def run_automatic():
    print("run robot AI")

def run_manual():
    print("run manual")

@app.after_request
def after_request(data):
    response = make_response(data)
    response.headers['Content-Type'] = 'application/json'
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers[
        'Access-Control-Allow-Headers'] = "Origin, X-Requested-With, Content-Type, Accept"
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE'
    return response


def bad_request(error):
    return make_response(jsonify({'error': 'Bad Request'}), 400)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not Found'}), 404)


if __name__ == '__main__':
    status = sys.argv[1]
    base_station_url = sys.argv[2]
    vision_regulator.set_url(base_station_url)

    app.register_blueprint(start_ai)
    app.register_blueprint(end_initial_orientation_task)
    app.register_blueprint(end_identify_antenna_task)
    app.register_blueprint(end_receive_information_task)
    app.register_blueprint(end_go_to_image_task)
    app.register_blueprint(end_take_picture_task)
    app.register_blueprint(end_go_to_drawzone_task)
    app.register_blueprint(end_draw_task)
    app.register_blueprint(end_go_out_of_drawzone_task)
    app.register_blueprint(end_light_red_led_task)

    if status == AUTOMATIC:
        print("AUTOMATIC MODE not implemented")
    elif status == MANUAL:
        print("MANUAL MODE")
        app.register_blueprint(go_to_position)
        app.register_blueprint(ledok.led_ok)

    else:
        print("Bad arguments : manual or automatic")
    app.run(host='0.0.0.0')
