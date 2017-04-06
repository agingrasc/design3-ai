from flask import Blueprint, make_response, jsonify, request

from mcu.regulator import PIDConstants


def create_regulator_constant_blueprint(regulator):
    regulator_constant = Blueprint('regulator_constnat', __name__)

    @regulator_constant.route("/regulator/constants", methods=["GET"])
    def get_regulator_constants():
        return make_response(jsonify(regulator.get_constants()))

    @regulator_constant.route("/regulator/constants", methods=["POST"])
    def set_regulator_constants():
        data = request.json

        new_constants = PIDConstants(
            data['kp'],
            data['ki'],
            data['kd'],
            data['theta_kp'],
            data['theta_ki'],
            data['position_deadzone'],
            data['max_cmd'],
            data['deadzone_cmd'],
            data['min_cmd'],
            data['theta_max_cmd'],
            data['theta_min_cmd']
        )

        regulator.set_constants(new_constants)

        return make_response(jsonify({"message": "constant change", "data": regulator.get_constants()}))

    return regulator_constant
