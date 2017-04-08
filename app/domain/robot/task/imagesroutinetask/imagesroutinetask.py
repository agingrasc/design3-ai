from domain.command.visionregulation import VisionRegulation
from domain.robot.blackboard import Blackboard
from domain.robot.task.drawtask.drawtask import DrawTask
from domain.robot.task.gooutofdrawzonetask.gooutofdrawzonetask import GoOutOfDrawzoneTask
from domain.robot.task.gotodrawzonetask.gotodrawzonetask import GoToDrawzoneTask
from domain.robot.task.task import Task
from service.globalinformation import GlobalInformation


class ImagesRoutineTask(Task):
    def __init__(self, global_information: GlobalInformation, blackboard: Blackboard,
                 vision_regulation: VisionRegulation, draw_task: DrawTask, go_to_drawzone_task: GoToDrawzoneTask
                 , go_out_of_drawzone_task: GoOutOfDrawzoneTask):

        self.global_information = global_information
        self.blackboard = blackboard
        self.vision_regulation = vision_regulation
        self.draw_task = draw_task
        self.go_to_drawzone_task = go_to_drawzone_task
        self.go_out_of_drawzone_task = go_out_of_drawzone_task


    def execute(self):
        for position in self.blackboard.images_position.values():
            self.vision_regulation.go_to_position(position)
            self.global_information.send_take_picture_request(0.5, "SOUTH")
            self.go_to_drawzone_task.execute()
            self.draw_task.execute()
