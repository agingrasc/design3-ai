import requests


class Feedback:
    def __init__(self, url: str):
        self.base_station_url = url

    def send_comment(self, comment: str):
        data = {'feedback': comment}
        requests.post(url=self.base_station_url, json=data)
