from flask import Blueprint, request, make_response, jsonify

chargetest = Blueprint('charge_test', __name__)

@chargetest.route('/charge_test_api', methods=['POST'])
def charge_test():
    data = request.data

    with open('../../../charge/picture_out.jpg', 'wb') as f:
        f.write(data)

    return make_response(jsonify({'status': "ok"}), 200)
