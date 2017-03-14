from .task.identifyantennatask import IdentifyAntennaTask
from .task.receiveinformationtask import ReceiveInformationTask
from .task.gotoimagetask import GoToImageTask
from .task.takepicturetask import TakePictureTask
from .task.gotodrawzonetask import GoToDrawzoneTask
from .task.drawtask import DrawTask
from .task.gooutofdrawzonetask import GoOutOfDrawzoneTask
from .task.lightredledtask import LightRedLedTask

class RobotAi():

    def __init__(self):
        self.robot_controller = None
        self.identify_antenna = IdentifyAntennaTask()
        self.receive_information = ReceiveInformationTask(self.robot_controller)
        self.go_to_image = GoToImageTask(self.robot_controller)
        self.take_picture = TakePictureTask(self.robot_controller)
        self.go_to_drawzone = GoToDrawzoneTask(self.robot_controller)
        self.draw = DrawTask(self.robot_controller)
        self.go_out_of_drawzone = GoOutOfDrawzoneTask(self.robot_controller)
        self.light_red_led = LightRedLedTask(self.robot_controller)

        self.x_robot_position = 10
        self.y_robot_position = 10

        self.tasks = {1: self.identify_antenna, 2: self.receive_information, 3: self.go_to_image, 4: self.take_picture
            , 5: self.go_to_drawzone, 6: self.draw, 7: self.go_out_of_drawzone, 8: self.light_red_led}


    def start(self, task = None):
        if(task):
            self._execute_one_task(task)
        else:
            self._execute()

    def _execute(self):
        for task_id in self.tasks:
            current_task = self.tasks[task_id]
            while current_task.status_flag == 0:
                self.robot_controller = current_task.execute(self.x_robot_position, self.y_robot_position)
            if current_task.status_flag == 1:
                continue

    def _execute_one_task(self, task_id):
        current_task = self.tasks[task_id]
        while current_task.status_flag == 0:
            self.robot_controller = current_task.execute(self.x_robot_position, self.y_robot_position)


