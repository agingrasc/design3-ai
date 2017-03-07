from .task import task

class identify_antenna(task):
    def __init__(self):
        task.__init__(self)
        self.x_start_point = 10
        self.y_start_point = 10
        self.x_end_point = 30
        self.y_end_point = 10
        self.x_max_point = 0
        self.y_max_point = 10

    def execute(self):
        print("indentifying antenna")
        print(self.id_image)
        print(self.magnification)
        print(self.orientation)
        self._go_to_start_point()
        self._go_to_end_point()
        self._go_to_max_point()

    def _go_to_start_point(self):
        print("going to start point")
        print(self.x_start_point)
        print(self.y_start_point)

    def _go_to_end_point(self):
        print("goint to end point")
        print(self.x_end_point)
        print(self.y_end_point)

    def _go_to_max_point(self):
        print("going to max point")
        print(self.x_max_point)
        print(self.y_max_point)