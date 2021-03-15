import random
import tkinter as tk
import tkinter.messagebox as mb
from tkinter import ttk

from PIL import Image, ImageTk, ImageDraw, ImageFont


class CustomImage:
    """Класс разрезания картинка"""

    def __init__(self, path, row=4, columns=4, pixels=160, font_path='./Font/news serif bolditalic.ttf'):
        self.size = (row * pixels, columns * pixels)
        self.pixels = pixels
        with Image.open(path) as image:
            self.image = image.resize(self.size).copy()

        self.row = row
        self.columns = columns
        self.font = ImageFont.truetype(font_path, int(pixels // 2 * 1.5))
        self.__crop__()
        self.add_all_text()

    def get_image(self, n):
        i = n // self.row
        j = n % self.columns
        return self.image_part[i][j]

    def add_all_text(self):
        columns = self.columns
        row = self.row
        for i in range(row):
            for j in range(columns):
                image = self.image_part[i][j]
                self.__add_text__(image, f'{i*4+j+1}')

    def __add_text__(self, image, text):
        draw = ImageDraw.Draw(image)
        font = self.font
        center = self.pixels // 3
        draw.text((center  - (len(text)-1)*self.pixels // 4, center), text, (255, 0, 0), font=font)

    def __crop__(self):
        columns = self.columns
        row = self.row
        pixels = self.pixels
        self.image_part = [[] for i in range(row)]
        image = self.image.copy()
        for i in range(row):
            for j in range(columns):
                left = j * pixels
                top = i * pixels
                right = left + pixels
                bottom = top + pixels
                self.image_part[i].append(image.crop((left, top, right, bottom)))


def get_row_column(n, row=4, columns=4):
    if n > 15:
        return None
    else:
        return n // row, n % columns


class Application(tk.Frame):
    """Класс игры"""
    def __init__(self, master=None, image='./Images/ny.jpg'):
        super().__init__(master)
        self.master.title('Пятнашки')
        self.style = ttk.Style()
        self.style.theme_use('alt')
        self.style.configure('TButton', background='plum1', foreground='white', focuscolor='none')
        self.style.map('TButton', background=[('active', 'spring green')])
        self.custom_image = CustomImage(image)

        self.master.grid_rowconfigure(1, weight=10)
        self.master.grid_columnconfigure(0, weight=10)

        self.create_menu_frame(0, 0)
        self.create_game_frame(1, 0)

        self.game_positions = {}
        self.start_game()

    def create_menu_frame(self, row, columns):
        self.Frame_menu = tk.Frame(self.master, bg='plum1')
        self.Frame_menu.grid(column=columns, row=row, sticky='nsew')
        self.Frame_menu.grid_columnconfigure(0, weight=1)
        self.Frame_menu.grid_columnconfigure(1, weight=1)

        # self.image = Image.open("./Images/enot.jpg").resize((40,40))

        self.Button_new_game = tk.Button(self.Frame_menu,
                                         text='New',
                                         width=10,
                                         height=2,
                                         bg="spring green",
                                         font=("Century Gothic", 12, 'bold'),
                                         command=self.start_game,
                                         )
        self.Button_new_game.grid(row=0, column=0, padx = 10)

        self.Button_exit = tk.Button(self.Frame_menu,
                                     text='Exit',
                                     width = 10,
                                     height = 2,
                                     bg="red",
                                     font=("Century Gothic", 12, 'bold'),
                                     command=self.quit
                                     )
        self.Button_exit.grid(row=0, column=1, padx = 10)

    def create_game_frame(self, row, columns):
        self.Frame_game = tk.Frame(self.master, background="plum1")
        self.Frame_game.grid(row=row, column=columns, sticky="nsew")
        self.Frame_game.bind('<Configure>', self._resize_image)

        self.Buttons = [[] for i in range(4)]
        self.Images = [[] for i in range(4)]
        self.Images_copy = [[] for i in range(4)]

        def move(i, j):
            return lambda: self.turn_button(i, j)

        for i in range(4):
            self.Frame_game.grid_rowconfigure(i, weight=2)
            self.Frame_game.grid_columnconfigure(i, weight=2)
            for j in range(4):
                if (i == 3 and j == 3):
                    self.Buttons[i].append(None)
                else:
                    n = i * 4 + j
                    self.Images[i].append(self.custom_image.get_image(n))
                    self.Images_copy[i].append(ImageTk.PhotoImage(self.Images[i][j].resize((30, 30))))
                    self.Buttons[i].append(ttk.Button(self.Frame_game,
                                                      command=move(i, j),
                                                      image=self.Images_copy[i][j],
                                                      ))

    def start_game(self):
        self.elements = [i for i in range(16)]
        self.position = [i for i in range(16)]
        random.shuffle(self.elements)
        random.shuffle(self.position)
        for n in range(16):
            el, pos = self.elements[n], self.position[n]
            el_i, el_j = get_row_column(el)
            pos_i, pos_j = get_row_column(pos)
            self.game_positions[(el_i, el_j)] = (pos_i, pos_j)
            if (self.Buttons[el_i][el_j]):
                self.Buttons[el_i][el_j].grid(row=pos_i, column=pos_j, sticky="nsew")
            else:
                self.add_available_move()
        if (self.is_win()):
            self.end_game()
        self.steps = 0

    def add_available_move(self):
        pos_i, pos_j = self.game_positions[(3, 3)]
        self.available_moves = []
        for a, b in [(0, 1), (1, 0), (-1, 0), (0, -1)]:
            tmp_i, tmp_j = pos_i + a, pos_j + b
            if 0 <= tmp_i < 4 and 0 <= tmp_j < 4:
                self.available_moves.append((tmp_i, tmp_j))

    def is_possible(self):
        N = 0
        for n in range(16):
            el, pos = self.elements[n], self.position[n]
            if el != 15:
                for m in range(16):
                    el_2, pos_2 = self.elements[m], self.position[m]
                    if el_2 < el and pos_2 > pos:
                        N += 1
            else:
                N += get_row_column(pos)[0] + 1
        return N % 2 == 0

    def turn_button(self, el_i, el_j):
        self.steps += 1
        pos_i, pos_j = self.game_positions[(el_i, el_j)]

        if (pos_i, pos_j) in self.available_moves:
            null_i, null_j = self.game_positions[(3, 3)]
            ## move button
            self.Buttons[el_i][el_j].grid(row=null_i, column=null_j, sticky="nsew")
            self.game_positions[(el_i, el_j)] = (null_i, null_j)

            ## "move" null
            self.game_positions[(3, 3)] = (pos_i, pos_j)
            self.add_available_move()

            if (self.is_win()):
                self.end_game()

    def is_win(self):
        for i in range(4):
            for j in range(4):
                if (self.game_positions[(i, j)] != (i, j)):
                    return False
        return True

    def end_game(self):
        if self.steps > 80:
            mb.showinfo("Победа!", f"Количество шагов: {self.steps}\nСтарайтесь лучше можно за 80 шагов")
        else:
            mb.showinfo("Победа!", f"Количество шагов: {self.steps}\nВы большой молодец")
        self.start_game()

    def _resize_image(self, event):
        new_width = event.width
        new_height = event.height
        for i in range(4):
            for j in range(4):
                if (i != 3 or j != 3) and (new_width // 4 > 9 and new_height // 4 > 9):
                    self.Images_copy[i][j] = ImageTk.PhotoImage(
                        self.Images[i][j].resize((new_width // 4 - 9, new_height // 4 - 9)))
                    self.Buttons[i][j].configure(image=self.Images_copy[i][j])


if __name__ == '__main__':
    app = Application()
    app.mainloop()
