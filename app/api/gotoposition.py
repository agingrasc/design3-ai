from flask import Blueprint, request, make_response, jsonify
from simulator.simulator import Simulator

go_to_position = Blueprint('go-to-position', __name__)
go_to_position_fake = Blueprint('go-to-position_fake', __name__)

@go_to_position.route('/go-to-position', methods=['POST'])
def go_to_position_():
    print("go-to-position")
    pos_x = request.json["x"]
    pos_y = request.json["y"]
    print(pos_x)
    print(pos_y)
    return make_response(jsonify({'x': pos_x, 'y': pos_y}), 200)

@go_to_position_fake.route('/go-to-position', methods=['POST'])
def go_to_position_fake_():
    simulator = Simulator()
    pos_x = request.json["x"]
    pos_y = request.json["y"]
    print("I am fake and Going to: (" + pos_x + ", " + pos_y + ")")
    simulator.simulate_going_to_position(pos_x, pos_y)
    return make_response(jsonify({'x': pos_x, 'y': pos_y}), 200)