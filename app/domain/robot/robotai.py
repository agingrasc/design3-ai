import json

class RobotAi:
    def __init__(self, global_information):
        self._global_information = global_information

    def execute(self, tasks_list):
        self._global_information.connection.send(json.dumps({"headers":"cycle_started"}))
        for task in tasks_list:
            print(task)
            task.execute()
        self._global_information.connection.send(json.dumps({"headers":"cycle_ended"}))