import requests as req
from flask import Blueprint, request, make_response, jsonify

BASE_STATION_API_URL = "http://192.168.0.30:12345/feedback"

send_feedback = Blueprint('send-feedback', __name__)

@send_feedback.route('/send-feedback', methods=['POST'])
def send_feedback_():
    data = request.json

    print(data["feedback"])

    req.post(url=BASE_STATION_API_URL, json=data)
    send_response = make_response(jsonify(), 200)
    return send_response