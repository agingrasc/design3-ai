from flask import Blueprint, send_file

chargetestreverse = Blueprint('charge_test_reverse', __name__)

@chargetestreverse.route('/charge_test_reverse', methods=['GET'])
def get_charge_test_reverse():
    print("get_charge_test")
    image = "../../../test1.jpg"


    return send_file(image, mimetype='image/png')
