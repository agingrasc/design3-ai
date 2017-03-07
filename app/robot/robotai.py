from task.identifyantenna import identify_antenna

class robot_ai():

    def start(self, task):
        self._execute(task)

    def _execute(self, task):
        if(task == 1):
            identify_antenna.execute();

