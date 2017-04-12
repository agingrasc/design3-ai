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
from domain.robot.task.imagesroutinetask.imagesroutinetask import ImagesRoutineTask
from domain.robot.task.identifyantennataskproxy.identifyantennataskproxy import IdentifyAntennaTaskProxy
from domain.robot.task.initialorientationtask.initialorientationtask import InitialOrientationTask
from domain.robot.task.lightredledtask.lightredledtask import LightRedLedTask
from domain.robot.task.receiveinformationtask.receiveinformationtask import ReceiveInformationTask
from domain.robot.task.shutdownredledtask.shutdownredledtask import ShutDownRedLedTask
from domain.robot.task.takepicturetask.takepicturetask import TakePictureTask
from service import pathfinding_application_service
from service.feedback import Feedback
from service.safezonefinder import SafeZoneFinder
from util.singleton import Singleton


class TaskFactory(metaclass=Singleton):
    def __init__(self, global_information, robot_controller):
        self.global_information = global_information
        self.robot_controller = robot_controller
        self.blackboard: Blackboard = Blackboard()
        self.feedback = Feedback(self.global_information)
        self.vision_regulation = VisionRegulation(self.robot_controller, self.global_information)
        self.drawer = Drawer(self.global_information, self.robot_controller, self.vision_regulation, self.blackboard)
        self.antenna = Antenna(self.global_information, self.robot_controller)
        self.decoder = Decoder(self.robot_controller)
        self.lighter = Lighter(self.robot_controller)
        self.safe_zone_finder = SafeZoneFinder(pathfinding_application_service, self.global_information)

    def create_initial_orientation_task(self):
        print(self.global_information)
        return InitialOrientationTask(self.feedback, self.vision_regulation, self.global_information)

    def create_indentify_antenna_task(self):
        return IdentifyAntennaTask(
            self.antenna, self.feedback, self.vision_regulation, self.global_information, self.blackboard, pathfinding_application_service
        )

    def create_receive_informations_task(self):
        return ReceiveInformationTask(self.feedback, self.decoder, self.vision_regulation, self.blackboard)

    def create_go_to_image_task(self):
        return GoToImageTask(
            self.feedback, self.vision_regulation, self.global_information, pathfinding_application_service,
            self.blackboard
        )

    def create_take_picture_task(self):
        return TakePictureTask(self.global_information, self.blackboard, self.feedback)

    def create_go_to_drawzone_task(self):
        return GoToDrawzoneTask(
            self.feedback, self.vision_regulation, self.global_information, pathfinding_application_service,
            self.blackboard
        )

    def create_draw_task(self):
        return DrawTask(self.feedback, self.drawer, self.global_information, self.blackboard)

    def create_go_out_of_drawzone_task(self):
        return GoOutOfDrawzoneTask(
            self.feedback, self.vision_regulation, self.global_information, self.safe_zone_finder
        )

    def create_light_red_led_task(self):
        return LightRedLedTask(self.feedback, self.lighter)

    def create_image_routine_task(self):
        return ImagesRoutineTask(self.global_information, self.blackboard, self.vision_regulation,
                                 self.create_draw_task(), self.create_go_to_drawzone_task()
                                 , self.create_go_out_of_drawzone_task())
    
    def create_shut_down_red_led_task(self):
        return ShutDownRedLedTask(self.feedback, self.lighter)

    def create_proxy_identify_antenna_task(self):
        return IdentifyAntennaTaskProxy(self.create_indentify_antenna_task(), self.blackboard,
                                        self.vision_regulation, self.global_information, pathfinding_application_service)

    def create_competition_tasks(self):
        return [
            self.create_shut_down_red_led_task(),
            self.create_initial_orientation_task(),
            self.create_proxy_identify_antenna_task(),
            self.create_receive_informations_task(),
            self.create_go_to_image_task(),
            self.create_take_picture_task(),
            self.create_go_to_drawzone_task(),
            self.create_draw_task(),
            self.create_go_out_of_drawzone_task(),
            self.create_light_red_led_task()
        ]

    def set_url(self, url: str):
        self.global_information.set_url(url)
