from domain.command.antenna import Antenna
from domain.command.decoder import Decoder
from domain.command.drawer import Drawer
from domain.command.lighter import Lighter
from domain.command.visionregulation import VisionRegulation
from domain.pathfinding import get_segments
from domain.robot.feedback import Feedback
from domain.robot.task.drawtask.drawtask import DrawTask
from domain.robot.task.gooutofdrawzonetask.gooutofdrawzonetask import GoOutOfDrawzoneTask
from domain.robot.task.gotodrawzonetask.gotodrawzonetask import GoToDrawzoneTask
from domain.robot.task.gotoimagetask.gotoimagetask import GoToImageTask
from domain.robot.task.identifyantennatask.identifyantennatask import IdentifyAntennaTask
from domain.robot.task.initialorientationtask.initialorientationtask import InitialOrientationTask
from domain.robot.task.lightredledtask.lightredledtask import LightRedLedTask
from domain.robot.task.receiveinformationtask.receiveinformationtask import ReceiveInformationTask
from domain.robot.task.takepicturetask import TakePictureTask
from mcu.robotcontroller import robot_controller, set_move_destination, RobotController
from service import pathfinding_application_service
from service.destinationcalculator import DestinationCalculator
from service.globalinformation import GlobalInformation
from service.image_position_finder import ImagePositionFinder

ROBOT_API_URL = "http://localhost:5000"


class TaskFactory():
    def __init__(self):
        self.robot_controler = RobotController()
        self.feedback = Feedback(ROBOT_API_URL)
        self.vision_regulation = VisionRegulation(robot_controller, set_move_destination)
        self.global_information = GlobalInformation()
        self.drawer = Drawer(self.robot_controler)
        self.antenna = Antenna(self.global_information, self.robot_controler)
        self.decoder = Decoder(self.robot_controler)
        self.image_position_finder = ImagePositionFinder()
        self.destination_calculator = DestinationCalculator(self.global_information)
        self.lighter = Lighter(self.robot_controler)
        self.task_list = []

    def create_initial_orientation_task(self):
        self.task_list.append(InitialOrientationTask(self.feedback, self.vision_regulation, self.global_information))
        return self.task_list

    def create_indentify_antenna_task(self):
        self.task_list.append(IdentifyAntennaTask(self.drawer, self.antenna, self.feedback, self.vision_regulation,
                                                  self.global_information))
        return self.task_list

    def create_receive_informations_task(self):
        self.task_list.append(ReceiveInformationTask(self.feedback, self.decoder))
        return self.task_list

    def create_go_to_image_task(self):
        self.task_list.append(GoToImageTask(self.feedback,
                                            self.vision_regulation,
                                            self.global_information,
                                            pathfinding_application_service,
                                            get_segments,
                                            self.image_position_finder))
        return self.task_list

    def create_take_picture_task(self):
        self.task_list.append(TakePictureTask(self.robot_controler))
        return self.task_list

    def create_go_to_drawzone_task(self):
        self.task_list.append(GoToDrawzoneTask(self.feedback,
                                               self.vision_regulation,
                                               self.global_information,
                                               pathfinding_application_service,
                                               get_segments))
        return self.task_list

    def create_draw_task(self):
        self.task_list.append(DrawTask(self.feedback, self.drawer))
        return self.task_list

    def create_go_out_of_drawzone_task(self):
        self.task_list.append(GoOutOfDrawzoneTask(self.feedback,
                                                  self.vision_regulation,
                                                  self.destination_calculator,
                                                  self.global_information,
                                                  pathfinding_application_service,
                                                  get_segments))
        return self.task_list

    def create_light_red_led_task(self):
        self.task_list.append(LightRedLedTask(self.feedback, self.lighter))
        return self.task_list

    def create_competition_tasks(self):
        self.task_list.append(InitialOrientationTask(self.feedback, self.vision_regulation, self.global_information))
        self.task_list.append(IdentifyAntennaTask(self.drawer, self.antenna, self.feedback, self.vision_regulation,
                                                  self.global_information))
        self.task_list.append(ReceiveInformationTask(self.feedback, self.decoder))
        self.task_list.append(GoToImageTask(self.feedback,
                                            self.vision_regulation,
                                            self.global_information,
                                            pathfinding_application_service,
                                            get_segments,
                                            self.image_position_finder))
        self.task_list.append(TakePictureTask(self.robot_controler))
        self.task_list.append(GoToDrawzoneTask(self.feedback,
                                               self.vision_regulation,
                                               self.global_information,
                                               pathfinding_application_service,
                                               get_segments))
        self.task_list.append(DrawTask(self.feedback, self.drawer))
        self.task_list.append(GoOutOfDrawzoneTask(self.feedback,
                                                  self.vision_regulation,
                                                  self.destination_calculator,
                                                  self.global_information,
                                                  pathfinding_application_service,
                                                  get_segments))
        self.task_list.append(LightRedLedTask(self.feedback, self.lighter))

        return self.task_list
