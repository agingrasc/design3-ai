import requests as req


class Feedback:
    def __init__(self, robot_api_url: str):
        self.robot_api_url = robot_api_url

    def send_comment(self, comment: str):
        pass
