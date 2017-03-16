from robot.task.drawtask import DrawTask
from robot.task.gooutofdrawzonetask import GoOutOfDrawzoneTask
from robot.task.gotodrawzonetask import GoToDrawzoneTask
from robot.task.gotoimagetask import GoToImageTask
from robot.task.identifyantennatask import IdentifyAntennaTask
from robot.task.lightredledtask import LightRedLedTask
from robot.task.receiveinformationtask import ReceiveInformationTask
from robot.task.takepicturetask import TakePictureTask


class TaskFactory():
    def __init__(self, robot_controler):
        self.robot_controler = robot_controler
        self.task_list = []

    def create_indentify_antenna_task(self):
        self.task_list.append(IdentifyAntennaTask(self.robot_controler))
        return self.task_list

    def create_receive_informations_task(self):
        self.task_list.append(ReceiveInformationTask(self.robot_controler))
        return self.task_list

    def create_go_to_image_task(self):
        self.task_list.append(GoToImageTask(self.robot_controler))
        return self.task_list

    def create_take_picture_task(self):
        self.task_list.append(TakePictureTask(self.robot_controler))
        return self.task_list

    def create_go_to_drawzone_task(self):
        self.task_list.append(GoToDrawzoneTask(self.robot_controler))
        return self.task_list

    def create_draw_task(self):
        self.task_list.append(DrawTask(self.robot_controler))
        return self.task_list

    def create_go_out_of_drawzone_task(self):
        self.task_list.append(GoOutOfDrawzoneTask(self.robot_controler))
        return self.task_list

    def create_light_red_led_task(self):
        self.task_list.append(LightRedLedTask(self.robot_controler))
        return self.task_list

    def create_competition_tasks(self):
        self.task_list.append(IdentifyAntennaTask(self.robot_controler))
        self.task_list.append(ReceiveInformationTask(self.robot_controler))
        self.task_list.append(GoToImageTask(self.robot_controler))
        self.task_list.append(TakePictureTask(self.robot_controler))
        self.task_list.append(GoToDrawzoneTask(self.robot_controler))
        self.task_list.append(DrawTask(self.robot_controler))
        self.task_list.append(GoOutOfDrawzoneTask(self.robot_controler))
        self.task_list.append(LightRedLedTask(self.robot_controler))

        return self.task_list