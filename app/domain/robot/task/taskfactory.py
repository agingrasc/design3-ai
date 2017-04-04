from domain.command.antenna import Antenna
from domain.command.decoder import Decoder
from domain.command.drawer import Drawer
from domain.command.lighter import Lighter
from domain.command.visionregulation import VisionRegulation
from domain.robot.blackboard import Blackboard
from domain.robot.task.drawtask.drawtask import DrawTask
from domain.robot.task.gooutofdrawzonetask.gooutofdrawzonetask import GoOutOfDrawzoneTask
from domain.robot.task.gotodrawzonetask.gotodrawzonetask import GoToDrawzoneTask
from domain.robot.task.gotoimagetask.gotoimagetask import GoToImageTask
from domain.robot.task.identifyantennatask.identifyantennatask import IdentifyAntennaTask
from domain.robot.task.initialorientationtask.initialorientationtask import InitialOrientationTask
from domain.robot.task.lightredledtask.lightredledtask import LightRedLedTask
from domain.robot.task.receiveinformationtask.receiveinformationtask import ReceiveInformationTask
from domain.robot.task.takepicturetask.takepicturetask import TakePictureTask
from mcu.robotcontroller import RobotController
from service import pathfinding_application_service
from service.feedback import Feedback
from service.globalinformation import GlobalInformation
from util.singleton import Singleton

ROBOT_API_URL = "http://localhost:5000"


class TaskFactory(metaclass=Singleton):
    def __init__(self):
        self.global_information = GlobalInformation()
        self.blackboard: Blackboard = Blackboard()
        self.feedback = Feedback(self.global_information)
        self.robot_controller = RobotController(self.global_information)
        self.vision_regulation = VisionRegulation(self.robot_controller, self.global_information)
        self.drawer = Drawer(self.global_information, self.robot_controller, self.vision_regulation)
        self.antenna = Antenna(self.global_information, self.robot_controller)
        self.decoder = Decoder(self.robot_controller)
        self.lighter = Lighter(self.robot_controller)
        self.task_list = []

    def create_initial_orientation_task(self):
        self.task_list.append(InitialOrientationTask(self.feedback, self.vision_regulation, self.global_information))
        return self.task_list

    def create_indentify_antenna_task(self):
        self.task_list.append(
            IdentifyAntennaTask(
                self.antenna, self.feedback, self.vision_regulation, self.global_information, self.blackboard
            )
        )
        return self.task_list

    def create_receive_informations_task(self):
        self.task_list.append(
            ReceiveInformationTask(self.feedback, self.decoder, self.vision_regulation, self.blackboard)
        )
        return self.task_list

    def create_go_to_image_task(self):
        self.task_list.append(
            GoToImageTask(
                self.feedback, self.vision_regulation, self.global_information, pathfinding_application_service,
                self.blackboard
            )
        )
        return self.task_list

    def create_take_picture_task(self):
        self.task_list.append(TakePictureTask(self.global_information, self.blackboard, self.feedback))
        return self.task_list

    def create_go_to_drawzone_task(self):
        self.task_list.append(
            GoToDrawzoneTask(
                self.feedback, self.vision_regulation, self.global_information, pathfinding_application_service,
                self.blackboard
            )
        )
        return self.task_list

    def create_draw_task(self):
        self.task_list.append(DrawTask(self.feedback, self.drawer, self.blackboard))
        return self.task_list

    def create_go_out_of_drawzone_task(self):
        self.task_list.append(
            GoOutOfDrawzoneTask(
                self.feedback, self.vision_regulation, self.global_information, pathfinding_application_service
            )
        )
        return self.task_list

    def create_light_red_led_task(self):
        self.task_list.append(LightRedLedTask(self.feedback, self.lighter))
        return self.task_list

    def create_competition_tasks(self):
        self.create_initial_orientation_task()
        self.create_indentify_antenna_task()
        self.create_receive_informations_task()
        self.create_go_to_image_task()
        self.create_take_picture_task()
        self.create_go_to_drawzone_task()
        self.create_draw_task()
        self.create_go_out_of_drawzone_task()
        self.create_light_red_led_task()
        return self.task_list

    def set_url(self, url: str):
        self.global_information.set_url(url)


task_factory = TaskFactory()
