import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as mb


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master.title('SmartWidget')
        self.available_figure = ['oval', 'rectangle']
        self.button_row = 2
        self.window_row = 1
        self.master.grid_rowconfigure(self.window_row, weight=20)
        for i in range(3):
            self.master.grid_columnconfigure(i, weight=1)
        for i in range(2, 5):
            self.master.grid_columnconfigure(i, weight=20)
        self.grid(sticky="nsew")

        self.TextWindow()
        self.DrawWindow()
        self.ComboxFigure()
        self.TextLabel()


        self.syncEdit = tk.Button(self.master, text="Рисовать из текста", command=self.GetFromText)
        self.syncEdit.grid(column=0, row=self.button_row, sticky="nsew")

        self.info_button = tk.Button(self.master, text='Требования к тексту', command = self.GetInfo)
        self.info_button.grid(column=1, row=self.button_row, sticky="nsew")

        self.syncGraph = tk.Button(self.master, text="Получить текст", command=self.GetText)
        self.syncGraph.grid(column=2, row=self.button_row, sticky="nsew")

        self.buttonClear = tk.Button(self.master, text="Отчистить", command=self.Clear)
        self.buttonClear.grid(column=3, row=self.button_row, sticky="nsew")

        self.exit_button = tk.Button(self.master, text='Выход', command=self.master.destroy)
        self.exit_button.grid(column=4, row=self.button_row, sticky="nsew")

    def ComboxFigure(self):
        self.figure_combox = ttk.Combobox(self.master, values=self.available_figure, state="readonly")
        self.figure_combox.grid(column=2, row=0, sticky="nsew")
        self.figure_combox.current(0)
        self.draw_function = self.canvas_window.create_oval
        self.figure = 'oval'
        self.figure_combox.bind("<<ComboboxSelected>>", self.SelectDrawFunction)

    def TextLabel(self):
        self.current_position_text = tk.StringVar()
        self.current_position_text.set('(0,0)')
        self.text_label = tk.Label(self.master, textvariable=self.current_position_text)
        self.text_label.grid(column=3, row=0, sticky="nsew")

    def SelectDrawFunction(self, event):
        self.figure = self.figure_combox.get()
        self.SetDrawFunction()

    def SetDrawFunction(self):
        if self.figure == 'oval':
            self.draw_function = self.canvas_window.create_oval
        elif self.figure == 'rectangle':
            self.draw_function = self.canvas_window.create_rectangle
        elif self.figure == 'line':
            self.draw_function = self.canvas_window.create_line

    def TextWindow(self):
        self.text_window = tk.Text(self.master, background="white")
        self.text_window.grid(column=0, row=self.window_row, columnspan=2,  sticky="nsew")
        self.text_window.tag_config("Err", background="red")

    def DrawWindow(self):
        self.canvas_window = tk.Canvas(self.master, background="white")
        self.canvas_window.grid(column=2, row=self.window_row, columnspan=3, sticky="nsew")
        self.canvas_window.bind('<Button-1>', self.Click)
        self.canvas_window.bind('<B1-Motion>', self.Draw)
        self.canvas_window.bind("<Motion>", self.Move)
        self.figure_dict = {}
        self.ClearFigureDict()
        self.grab_figure = None

    def GetFromText(self):
        self.canvas_window.delete("all")
        self.ClearFigureDict()
        lines = self.text_window.get('1.0', 'end-1c').split('\n')
        for i, line in enumerate(lines, 1):
            if line.strip() == "":
                continue
            text_figure = list(map(str.strip, line.split(';')))
            self.text_window.tag_remove("Err", f"{i}.0", f"{i}.end")
            try:
                figure = text_figure[0]
                if figure == 'oval':
                    text_function = 'self.canvas_window.create_oval'
                elif figure == 'rectangle':
                    text_function = 'self.canvas_window.create_rectangle'
                elif figure == 'line':
                    text_function = 'self.canvas_window.create_line'
                else:
                    raise
                min_x, min_y, max_x, max_y = map(float, text_figure[1].lstrip('<').rstrip('>').split(' '))
                width = text_figure[2]
                border = text_figure[3]
                fill = text_figure[4]

                eval(
                    f'self.figure_dict["{figure}"].append({text_function}(min_x,min_y,max_x,max_y, width="{width}", outline="{border}", fill="{fill}"))')
            except:
                self.text_window.tag_add("Err", f"{i}.0", f"{i}.end")

    def ClearFigureDict(self):
        for figure in self.available_figure:
            self.figure_dict[figure] = []

    def GetText(self):
        self.text_window.delete('1.0', tk.END)
        for key, values in self.figure_dict.items():
            for figure in values:
                figure_string = ""
                figure_string += f"{key}; "
                figure_coords = self.canvas_window.coords(figure)
                figure_string += '<'+' '.join(list(map(str, figure_coords)))+'>; '
                figure_string += str(self.canvas_window.itemcget(figure, "width")) + "; "
                figure_string += str(self.canvas_window.itemcget(figure, "outline")) + "; "
                figure_string += str(self.canvas_window.itemcget(figure, "fill")) + "\n"
                self.text_window.insert("end", figure_string)

    def Click(self, event):
        self.current_position = (event.x, event.y)
        self.grab_figure = self.canvas_window.find_overlapping(event.x, event.y, event.x, event.y)
        self.clicked = 1

    def Draw(self, event):
        if not (self.grab_figure):
            if self.clicked:
                self.figure_dict[self.figure].append(
                    self.draw_function(self.current_position[0], self.current_position[1], event.x, event.y, fill="purple1"))
                self.clicked = 0
            else:
                if event.x < 1:
                    x = max(event.x, 1)
                elif event.x >= self.canvas_window.winfo_width():
                    x = min(event.x, self.canvas_window.winfo_width()-1)
                else:
                    x = event.x
                if event.y < 1:
                    y = max(event.y, 1)
                elif event.y >= self.canvas_window.winfo_height():
                    y = min(event.y, self.canvas_window.winfo_height()-1)
                else:
                    y = event.y

                self.canvas_window.coords(self.figure_dict[self.figure][-1], self.current_position[0],
                                          self.current_position[1], x, y)
                self.current_position_text.set(f"({event.x}, {event.y})")
        else:
            if (event.x < self.canvas_window.winfo_width() and event.x > 0) and \
                    (event.y < self.canvas_window.winfo_height() and event.y > 0):
                self.canvas_window.move(self.grab_figure[-1], event.x - self.current_position[0],
                                       event.y - self.current_position[1])
                self.current_position = [event.x, event.y]
                self.current_position_text.set(f"({event.x}, {event.y})")

    def Move(self, event):
        self.current_position_text.set(f"({event.x}, {event.y})")

    def Clear(self):
        self.current_position_text.set('(0,0)')
        self.canvas_window.delete("all")
        self.ClearFigureDict()
        self.grab_figure = None

    def GetInfo(self):
        mb.showinfo(f'Требования к тексту объекта', 'Следующие требования:'
                                                    f'\n 1. Разделения через символ ";"'
                                                    f'\n 2. Порядок: type; coords; width; outline; fill'
                                                    f'\n 3. Доступные type: {self.available_figure}'
                                                    f'\n 4. Запись coords: <float float float float>'
                                                    f'\n 5. Запись width: float'
                                                    f'\n 6. Запись outline и fill: Текст или 16-ричное число'
                                                    f'\n Пример: oval; <3.1 2.5 150 320>; 10; blue; #b1ff00'
                    )


app = Application()
app.mainloop()