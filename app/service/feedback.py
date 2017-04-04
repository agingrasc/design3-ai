import json
import requests

from service.globalinformation import GlobalInformation, BASE_URL_PATTERN

END_POINT_PATH = "feedback-task"

TASK_IDENTEFIE_ANTENNA = "identifie_antenna"
TASK_RECEIVE_INFORMATION = "receive_informations"
TASK_GO_TO_IMAGE = "go_to_image"
TASK_TAKE_PICTURE = "take_picture"
TASK_GO_TO_DRAWING_ZONE = "go_to_drawing_zone"
TASK_DRAW_IMAGE = "draw_image"
TASK_GO_OUT_OF_DRAWING_ZONE = "go_out_of_drawing_zone"
TASK_INITIAL_ORIENTATION = "intitial_orientation"
TASK_LIGHT_RED_LED = "light_red_led"


class Feedback:
    def __init__(self, global_information: GlobalInformation):
        self.global_information = global_information

    def send_comment(self, comment: str):
        data = {}
        data["task_name"] = comment
        value = {}
        value["headers"] = "push_tasks_information"
        value["data"] = data
        self.global_information.connection.send(json.dumps(value))

    def send_new_cycle(self):
        value = {}
        value["headers"] = "new_round"
        value["data"] = {}
        self.global_information.connection.send(json.dumps(value))
