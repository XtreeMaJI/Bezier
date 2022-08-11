import tkinter as tk
import Point
import Bezier
from typing import List

exit_flag = False
root: tk.Tk = None
points: List[Point.Point] = []
dragging_point: Point.Point = None
bezier: Bezier.Bezier = None
main_canvas: tk.Canvas = None
is_draw_helper_lines: tk.BooleanVar = None


def on_close_window():
    global exit_flag
    exit_flag = True


def on_lmb_press(event, canvas: tk.Canvas):
    global dragging_point
    mouse_x = canvas.winfo_pointerx() - canvas.winfo_rootx()
    mouse_y = canvas.winfo_pointery() - canvas.winfo_rooty()
    point_size = Point.point_size
    #Проверяем пересечение с точками
    for p in points:
        if p.x - point_size < mouse_x < p.x + point_size and p.y - point_size < mouse_y < p.y + point_size:
            dragging_point = p
            break


def on_lmb_release(event):
    global dragging_point
    dragging_point = None


def drag_point(p: Point.Point, canvas: tk.Canvas):
    mouse_x = canvas.winfo_pointerx() - canvas.winfo_rootx()
    mouse_y = canvas.winfo_pointery() - canvas.winfo_rooty()
    p.set_pos(mouse_x, mouse_y)


def change_num_of_bezier_points(event, slider: tk.Scale):
    bezier.num_of_points = int(bezier.max_num_of_points*slider.get())
    redraw_main_canvas()


def redraw_main_canvas():
    global main_canvas
    main_canvas.delete("all")
    for p in points:
        p.draw()
    bezier.draw()


def on_helper_lines_cb_press():
    global is_draw_helper_lines
    bezier.is_draw_helper_lines = is_draw_helper_lines.get()
    redraw_main_canvas()

def main():
    global exit_flag
    global root
    global dragging_point
    global points
    global bezier
    global main_canvas
    global is_draw_helper_lines

    Point.point_size = 10

    root = tk.Tk()
    root.protocol("WM_DELETE_WINDOW", on_close_window)

    main_canvas = tk.Canvas(root, width=1920, height=1080, bg="white")
    main_canvas.grid(row=0, column=1)

    interface_frame = tk.Frame(root)
    interface_frame.grid(row=0, column=0, sticky="N")

    #Слайдер для последней нарисованной точки
    current_t_text = tk.Text(interface_frame, width=24, height=1, bg=root["background"], borderwidth=0)
    current_t_text.insert(tk.INSERT, "Доля нарисованных точек")
    current_t_text.grid(row=0, column=0, sticky="EW")
    current_t_slider = tk.Scale(interface_frame, from_=0, to=1.0, resolution=0.01, orient=tk.HORIZONTAL)
    current_t_slider.grid(row=1, column=0, sticky="EW")
    current_t_slider.set(1)

    #Чекбоксы для вспомогательных линий
    #Линии между контрольными точками и якорями, а также последние нарисованные точки на них
    is_draw_helper_lines_text = tk.Text(interface_frame, width=24, height=1, bg=root["background"], borderwidth=0)
    is_draw_helper_lines_text.insert(tk.INSERT, "Вспомогательные линии")
    is_draw_helper_lines_text.grid(row=2, column=0, sticky="EW")
    is_draw_helper_lines = tk.BooleanVar()
    is_draw_helper_lines_cb = tk.Checkbutton(interface_frame, variable=is_draw_helper_lines, command=on_helper_lines_cb_press)
    is_draw_helper_lines_cb.grid(row=3, column=0, sticky="EW")

    p1 = Point.Point(100, 500, "blue", main_canvas)
    p2 = Point.Point(1300, 300, "blue", main_canvas)
    p3 = Point.Point(225, 200, "blue", main_canvas)
    p4 = Point.Point(600, 700, "blue", main_canvas)

    bezier = Bezier.Bezier("green", main_canvas, 100)
    bezier.add_anchor_point(p1)
    bezier.add_anchor_point(p2)
    bezier.add_control_point(p3)
    bezier.add_control_point(p4)
    bezier.draw()

    p1.draw()
    p2.draw()
    p3.draw()
    p4.draw()

    points.append(p1)
    points.append(p2)
    points.append(p3)
    points.append(p4)

    main_canvas.bind("<ButtonPress-1>", lambda event, can=main_canvas: on_lmb_press(event, can))
    main_canvas.bind("<ButtonRelease-1>", on_lmb_release)

    current_t_slider.bind("<B1-Motion>", lambda event, s=current_t_slider: change_num_of_bezier_points(event, s))

    while not exit_flag:
        root.update()
        if dragging_point is not None:
            drag_point(dragging_point, main_canvas)
            redraw_main_canvas()


if __name__ == "__main__":
    main()
