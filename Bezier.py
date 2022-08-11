import Point


class Bezier:

    def __init__(self, new_color, new_canvas, new_num_of_points):
        self.color = new_color
        self.canvas = new_canvas
        self.max_num_of_points = new_num_of_points
        self.num_of_points = new_num_of_points
        self.anchor_points = []
        self.control_points = []
        self.is_draw_helper_lines = False

    def lerp(self, p1=Point.Point(), p2=Point.Point(), t=0):
        lerped_x = p1.x + (p2.x - p1.x) * t
        lerped_y = p1.y + (p2.y - p1.y) * t
        p3 = Point.Point(lerped_x, lerped_y, self.color, self.canvas)
        return p3

    def add_anchor_point(self, p=Point.Point()):
        self.anchor_points.append(p)

    def add_control_point(self, p=Point.Point()):
        self.control_points.append(p)

    def draw(self):
        prev_point = self.anchor_points[0]

        for i in range(0, self.num_of_points+1, 1):
            #Лерпы между всеми первоначальными точками
            p12 = self.lerp(self.anchor_points[0], self.control_points[0], i/self.max_num_of_points)
            p23 = self.lerp(self.control_points[0], self.control_points[1], i/self.max_num_of_points)
            p34 = self.lerp(self.control_points[1], self.anchor_points[1], i/self.max_num_of_points)

            #Лерпы между лерпами первоначальных точек
            p1 = self.lerp(p12, p23, i/self.max_num_of_points)
            p2 = self.lerp(p23, p34, i/self.max_num_of_points)

            cur_point = self.lerp(p1, p2, i/self.max_num_of_points)

            self.canvas.create_line(prev_point.x, prev_point.y, cur_point.x, cur_point.y, fill=self.color, width=4)

            if self.is_draw_helper_lines:
                self.canvas.create_line(self.anchor_points[0].x, self.anchor_points[0].y,
                                        self.control_points[0].x, self.control_points[0].y, fill="purple")

                self.canvas.create_line(self.control_points[0].x, self.control_points[0].y,
                                        self.control_points[1].x, self.control_points[1].y, fill="purple")

                self.canvas.create_line(self.control_points[1].x, self.control_points[1].y,
                                        self.anchor_points[1].x, self.anchor_points[1].y, fill="purple")

                if i == self.num_of_points:
                    self.canvas.create_line(p12.x, p12.y, p23.x, p23.y, fill="purple")
                    self.canvas.create_line(p23.x, p23.y, p34.x, p34.y, fill="purple")
                    self.canvas.create_line(p1.x, p1.y, p2.x, p2.y, fill="purple")
                    p12.draw()
                    p23.draw()
                    p34.draw()
                    p1.draw()
                    p2.draw()
                    cur_point.draw()

            prev_point = cur_point