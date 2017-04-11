from domain.robot.blackboard import Blackboard
from domain.robot.task.task import Task
from domain.command.drawer import Drawer
from service.feedback import Feedback
from service.globalinformation import GlobalInformation
from service.feedback import TASK_DRAW_IMAGE
from service.segmentwrapper import SegmentWrapper

MESSAGE = "End of drawing task!"


class DrawTask(Task):
    def __init__(self, feedback: Feedback, drawer: Drawer, global_information: GlobalInformation, segment_wrapper: SegmentWrapper):
        super().__init__()
        self.drawer = drawer
        self.feedback = feedback
        self.global_information = global_information
        self.segment_wrapper = segment_wrapper

    def execute(self):
        draw_path = self.segment_wrapper.wrap_segment()
        self.global_information.send_path(draw_path )
        self.drawer.draw(draw_path)
        self.feedback.send_comment(TASK_DRAW_IMAGE)