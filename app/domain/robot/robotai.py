class RobotAi:
    def execute(self, tasks_list):
        for task in tasks_list:
            print(task)
            task.execute()
