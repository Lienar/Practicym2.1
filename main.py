import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox
from PIL import Image, ImageDraw


class DrawingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Рисовалка с сохранением в PNG")

        self.image = Image.new("RGB", (600, 400), "white")
        self.draw = ImageDraw.Draw(self.image)

        self.canvas = tk.Canvas(root, width=600, height=400, bg='white')
        self.canvas.pack()

        self.setup_ui()

        self.last_x, self.last_y = None, None
        self.pen_color = 'black'

        self.canvas.bind('<B1-Motion>', self.paint)
        self.canvas.bind('<ButtonRelease-1>', self.reset)

    def setup_ui(self):
        scale_min = 1
        scale_max = 21
        ''' Ввод дополнительный параметров '''
        control_frame = tk.Frame(self.root)
        control_frame.pack(fill=tk.X)

        clear_button = tk.Button(control_frame, text="Очистить", command=self.clear_canvas)
        clear_button.pack(side=tk.LEFT)

        color_button = tk.Button(control_frame, text="Выбрать цвет", command=self.choose_color)
        color_button.pack(side=tk.LEFT)

        save_button = tk.Button(control_frame, text="Сохранить", command=self.save_image)
        save_button.pack(side=tk.LEFT)

        brush_size_menu = self.brush_size_menu(control_frame, scale_min, scale_max)
        ''' Вызов функции создания меню '''
        brush_size_menu.config(width=5, font=("Helvetica", 12))
        ''' Отрисовка меню '''
        brush_size_menu.pack(side=tk.LEFT)
        ''' Установка расположения меню '''
        self.brush_size_scale = tk.Scale(control_frame, from_=scale_min, to=scale_max, orient=tk.HORIZONTAL)
        self.brush_size_scale.pack(side=tk.LEFT)

    def paint(self, event):
        if self.last_x and self.last_y:
            self.canvas.create_line(self.last_x, self.last_y, event.x, event.y,
                                    width=self.brush_size_scale.get(), fill=self.pen_color,
                                    capstyle=tk.ROUND, smooth=tk.TRUE)
            self.draw.line([self.last_x, self.last_y, event.x, event.y], fill=self.pen_color,
                           width=self.brush_size_scale.get())

        self.last_x = event.x
        self.last_y = event.y

    def reset(self, event):
        self.last_x, self.last_y = None, None

    def clear_canvas(self):
        self.canvas.delete("all")
        self.image = Image.new("RGB", (600, 400), "white")
        self.draw = ImageDraw.Draw(self.image)

    def choose_color(self):
        self.pen_color = colorchooser.askcolor(color=self.pen_color)[1]

    def save_image(self):
        file_path = filedialog.asksaveasfilename(filetypes=[('PNG files', '*.png')])
        if file_path:
            if not file_path.endswith('.png'):
                file_path += '.png'
            self.image.save(file_path)
            messagebox.showinfo("Информация", "Изображение успешно сохранено!")

    def brush_size_menu(self, control_frame, scale_min, scale_max):
        """ Функция создания меню """
        optionlist = []
        if scale_max - scale_min <= 10:
            for i in range(scale_min, scale_max+1):
                optionlist.append(f'{i}')
        elif 10 < scale_max - scale_min <= 20:
            for i in range(scale_min, scale_max + 1, 2):
                optionlist.append(f'{i}')
        else:
            step = int((scale_max - scale_min)/10)
            for i in range(scale_min, scale_max + 1, step):
                optionlist.append(f'{i}')
        ''' Значение параметров размера кисти '''
        variable = tk.StringVar(control_frame)
        variable.set(optionlist[0])
        ''' Задание параметров кисти '''
        brush_menu = tk.OptionMenu(control_frame, variable, *optionlist)
        ''' Отрисовка выпадающего меню '''
        def menu_callback(*data):
            data1 = variable.get()
            self.brush_size_scale.set(int(data1))
        ''' Функция настройки размера кисти'''
        variable.trace("w", menu_callback)
        ''' Отслеживания выбора элемента меню'''
        return brush_menu


def main():
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()