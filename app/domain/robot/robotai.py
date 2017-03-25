
class RobotAi():

    def __init__(self, task_execute_list):
        self.task_execute_list = task_execute_list

    def execute(self):
        for task in self.task_execute_list:
            task.execute()


