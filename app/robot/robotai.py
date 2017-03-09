from .task.identifyantenna import identify_antenna
from .task.receiveinformation import receive_information
from .task.gotoimage import go_to_image
from .task.takepicture import take_picture
from .task.gotodrawzone import go_to_drawzone
from .task.draw import draw
from .task.endcycle import end_cycle

class robot_ai():

    def __init__(self):
        self.robot_controller = None
        self.identify_antenna = identify_antenna()
        self.receive_information = receive_information(self.robot_controller)
        self.go_to_image = go_to_image(self.robot_controller)
        self.take_picture = take_picture(self.robot_controller)
        self.go_to_drawzone = go_to_drawzone(self.robot_controller)
        self.draw = draw(self.robot_controller)
        self.end_cycle = end_cycle(self.robot_controller)

        self.x_robot_position = 20
        self.y_robot_position = 40


    def start(self, task):

        self._execute(task)

    def _execute(self, task_id):
        tasks = {1: self.identify_antenna, 2: self.receive_information, 3: self.go_to_image, 4: self.take_picture
                 , 5: self.go_to_drawzone, 6: self.draw, 7: self.end_cycle}
        current_task = tasks[task_id]
        for task_id in tasks:
            while current_task.status_flag == 0:
                self.robot_controller = current_task.execute(self.x_robot_position, self.y_robot_position)
            if current_task.status_flag == 1:
                continue
        # if(task_id == 1):
        #     identification = identify_antenna()
        #     identification.execute()



