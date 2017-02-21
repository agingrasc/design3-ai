from flask import Blueprint, request, make_response, jsonify

chargetest = Blueprint('charge_test', __name__)

@chargetest.route('/charge-test_api', methods=['POST'])
def charge_test():
    print("charge_test")
    data = request.data
    print(data)
    return make_response(jsonify({'status': "ok"}), 200)
