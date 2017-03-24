import requests as req
from flask import  make_response, jsonify
import json


class Feedback:
    def __init__(self, robot_api_url: str):
        self.robot_api_url = robot_api_url

    def send_comment(self, comment: str):
        data =  {"feedback" : comment}

        json_data = json.dumps(data)

        req.post(url=self.robot_api_url + "/send_feedback", json=json_data)
        send_response = make_response(jsonify(), 200)
        return send_response
