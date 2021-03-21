import tkinter as tk
from tkinter import font


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master.title('InputLabel')
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        self.grid(sticky="news")
        self.create_widgets()
        for column in range(self.grid_size()[0]):
            self.columnconfigure(column, weight=1)
        for row in range(self.grid_size()[1]):
            self.rowconfigure(row, weight=1)

    def create_widgets(self):
        self.labelText = InputLabel(self)
        self.labelText.grid(sticky="nsew")

        self.buttonQuit = tk.Button(self, text="Quit", command=self.master.quit)
        self.buttonQuit.grid()


class InputLabel(tk.Label):
    def __init__(self, master=None):
        self.string_row = tk.StringVar()
        self.string_len = 0
        self.font_size = 16
        self.text_font = font.Font(family='Century Gothic', size=self.font_size, weight='normal')
        super().__init__(master,
                         cursor="arrow",
                         relief="sunken",
                         font=self.text_font,
                         takefocus=1,
                         textvariable=self.string_row,
                         anchor=tk.NW)
        ## Подбором
        label_height = self.font_size + 2
        label_width = 1
        self.border = tk.Frame(self, background="black", height=label_height, width=label_width)
        self.border_x = 0
        self.letter_position = 0
        self.border_y = self.font_size // 3
        self.border.place(x=self.border_x, y=self.border_y)

        self.is_border_off = False
        self.border_off()

        self.bind('<Key>', self.key_clicked)
        self.bind('<Button-1>', self.mouse_clicked)

    def get_text_size(self, letter='0'):
        text_len = self.text_font.measure(letter)
        return text_len

    def border_off(self):
        if self.is_border_off:
            self.border.configure(background=self.master['background'])
        else:
            self.border.configure(background="black")

        self.is_border_off = not self.is_border_off
        self.master.after(488, self.border_off)

    def key_clicked(self, event):
        if event.keysym == "Right":
            self.border_change_position(self.letter_position + 1)
        elif event.keysym == "Left":
            self.border_change_position(self.letter_position - 1)
        elif event.keysym == "Home":
            self.border_change_position(0)
        elif event.keysym == "End":
            self.border_change_position(len(self.string_row.get()))
        elif event.keysym == 'BackSpace':
            if self.border_x > 0:
                self.string_row.set(self.string_row.get()[:self.letter_position - 1] +
                                    self.string_row.get()[self.letter_position:])
                self.border_change_position(self.letter_position - 1)
        elif event.char:
            self.string_row.set(self.string_row.get()[:self.letter_position] +
                                event.char +
                                self.string_row.get()[self.letter_position:])
            self.border_change_position(self.letter_position + 1)

    def mouse_clicked(self, event):
        self.focus_set()
        curr_x = event.x
        string_row_text = self.string_row.get()
        new_position, new_x = 0, 0
        last_postion, last_x = 0, 0
        part_text = ''
        for l in string_row_text:
            part_text += l
            new_position += 1
            new_x = self.get_text_size(part_text)
            if new_x >= curr_x:
                if abs(curr_x - new_x) <= abs(curr_x - last_x):
                    self.border_change_position(new_position)
                else:
                    self.border_change_position(last_postion)
                break
            else:
                last_postion, last_x = new_position, new_x

    def border_change_position(self, position):
        string_row_text = self.string_row.get()
        len_string = len(string_row_text)
        if position > len_string:
            return
        self.letter_position = position
        self.border_x = self.get_text_size(string_row_text[:self.letter_position])
        self.border.place(x=self.border_x, y=self.border_y)


app = Application()
app.mainloop()
