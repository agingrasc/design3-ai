import requests

from service.globalinformation import GlobalInformation, BASE_URL_PATTERN

END_POINT_PATH = "feedback-task"


class Feedback:
    def __init__(self, global_information: GlobalInformation):
        self.global_information = global_information

    def send_comment(self, comment: str):
        data = {'feedback': comment}
        requests.post(url=BASE_URL_PATTERN.format(self.global_information.base_station_url, END_POINT_PATH), json=data)
