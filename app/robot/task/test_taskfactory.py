from unittest import TestCase
from unittest.mock import Mock, MagicMock, patch, call

from mcu.robotcontroller import RobotController
from robot.task.drawtask import DrawTask
from robot.task.gooutofdrawzonetask import GoOutOfDrawzoneTask
from robot.task.gotodrawzonetask import GoToDrawzoneTask
from robot.task.gotoimagetask import GoToImageTask
from robot.task.identifyantennatask import IdentifyAntennaTask
from robot.task.initialorientationtask import InitialOrientationTask
from robot.task.lightredledtask import LightRedLedTask
from robot.task.receiveinformationtask import ReceiveInformationTask
from robot.task.takepicturetask import TakePictureTask
from robot.task.taskfactory import TaskFactory


class TaskFactoryTest(TestCase):

    def setUp(self):
        self.robot_controler = Mock(RobotController)
        self.task_factory = TaskFactory(self.robot_controler)

    def test_can_create_an_initial_orientation_task(self):

        task_list = self.task_factory.create_initial_orientation_task()

        self.assertEquals(len(task_list), 1)
        self.assertTrue(type(task_list[0]) is InitialOrientationTask)

    def test_can_create_an_identify_antenna_task(self):
        task_list = self.task_factory.create_indentify_antenna_task()

        self.assertEquals(len(task_list), 1)
        self.assertTrue(type(task_list[0]) is IdentifyAntennaTask)

    def test_can_create_a_receive_information_task(self):
        task_list = self.task_factory.create_receive_informations_task()

        self.assertEquals(len(task_list), 1)
        self.assertTrue(type(task_list[0]) is ReceiveInformationTask)

    def test_can_create_a_go_to_image_task(self):
        task_list = self.task_factory.create_go_to_image_task()

        self.assertEquals(len(task_list), 1)
        self.assertTrue(type(task_list[0]) is GoToImageTask)

    def test_can_create_a_take_picture_task(self):
        task_list = self.task_factory.create_take_picture_task()

        self.assertEquals(len(task_list), 1)
        self.assertTrue(type(task_list[0]) is TakePictureTask)

    def test_can_create_a_go_to_drawzone_task(self):
        task_list = self.task_factory.create_go_to_drawzone_task()

        self.assertEquals(len(task_list), 1)
        self.assertTrue(type(task_list[0]) is GoToDrawzoneTask)

    def test_can_create_a_draw_task(self):
        task_list = self.task_factory.create_draw_task()

        self.assertEquals(len(task_list), 1)
        self.assertTrue(type(task_list[0]) is DrawTask)

    def test_can_create_a_go_out_of_drawzone_task(self):
        task_list = self.task_factory.create_go_out_of_drawzone_task()

        self.assertEquals(len(task_list), 1)
        self.assertTrue(type(task_list[0]) is GoOutOfDrawzoneTask)

    def test_can_create_a_light_red_led_task(self):
        task_list = self.task_factory.create_light_red_led_task()

        self.assertEquals(len(task_list), 1)
        self.assertTrue(type(task_list[0]) is LightRedLedTask)

    def test_can_create_all_competition_tasks(self):
        task_list = self.task_factory.create_competition_tasks()

        self.assertEquals(len(task_list), 9)
        self.assertTrue(type(task_list[0]) is InitialOrientationTask)
        self.assertTrue(type(task_list[1]) is IdentifyAntennaTask)
        self.assertTrue(type(task_list[2]) is ReceiveInformationTask)
        self.assertTrue(type(task_list[3]) is GoToImageTask)
        self.assertTrue(type(task_list[4]) is TakePictureTask)
        self.assertTrue(type(task_list[5]) is GoToDrawzoneTask)
        self.assertTrue(type(task_list[6]) is DrawTask)
        self.assertTrue(type(task_list[7]) is GoOutOfDrawzoneTask)
        self.assertTrue(type(task_list[8]) is LightRedLedTask)


