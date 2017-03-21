
class RobotAi():

    def __init__(self, task_execute_list):
        self.task_execute_list = task_execute_list
        self.x_robot_position = 10
        self.y_robot_position = 10

    def execute(self):
        for task in self.task_execute_list:
            while task.status_flag == 0:
                task.execute(self.x_robot_position, self.y_robot_position)


