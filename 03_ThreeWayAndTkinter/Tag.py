import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk,ImageDraw, ImageFont
import tkinter.messagebox as mb

import random
class CustomImage():
    def __init__(self, path, row=4, columns=4, pixels = 160, font_path = './Font/news serif bolditalic.ttf'):
        self.size = (row * pixels,  columns * pixels)
        print(self.size)
        self.pixels = pixels
        with Image.open(path) as image:
            self.image = image.resize(self.size).copy()

        self.row = row
        self.columns = columns
        self.font = ImageFont.truetype(font_path, int(pixels// 2 * 1.5))
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
                self.__add_text__(image, f'{i*4+j}')

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



class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        self.custom_image = CustomImage('./Images/enot.jpg')

        self.s = ttk.Style()
        self.s.configure('TButton', anchor=tk.W)
        self.master.grid_rowconfigure(1, weight=10)
        self.master.grid_columnconfigure(0, weight=10)

        self.create_menu_frame(0, 0)

        self.create_game_frame(1, 0)

        # Show image using label


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
                                         bg = "spring green",
                                         font = ("Century Gothic", 12, 'bold'),
                                         command=self.new_game,
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
        self.Frame_game = tk.Frame(self.master, background="pink")
        self.Frame_game.grid(row=row, column=columns, sticky="nsew")
        for i in range(4):
            self.Frame_game.grid_rowconfigure(i, weight=2)
            self.Frame_game.grid_columnconfigure(i, weight=2)

        self.Buttons = [[] for i in range(4)]
        self.Images = [[] for i in range(4)]
        self.Images_copy = [[] for i in range(4)]
        self.Frame_game.bind('<Configure>', self._resize_image)

        for i in range(4):
            for j in range(4):
                if (i == 3 and j == 3):
                    self.Buttons[i].append(None)
                else:
                    el = i * 4 + j
                    self.Images[i].append(self.custom_image.get_image(el))
                    self.Images_copy[i].append(ImageTk.PhotoImage(self.Images[i][j].resize((40, 40))))
                    self.Buttons[i].append(ttk.Button(self.Frame_game,
                                         width=40,
                                         # height=40,
                                         # bg = "spring green",
                                         command=self.new_game,
                                                     image=self.Images_copy[i][j],
                                         ))
                    self.Buttons[i][j].grid(row=i, column=j, padx = 5, pady=5, sticky="nsew")


        self.gameMap = {}

    def _resize_image(self,event):
        new_width = event.width
        new_height = event.height

        for i in range(4):
            for j in range(4):
                if (i == 3 and j == 3):
                    continue
                self.Images_copy[i][j] = ImageTk.PhotoImage(self.Images[i][j].resize((new_width // 5, new_height // 5)))
                self.Buttons[i][j].configure(image=self.Images_copy[i][j])

        # self.background_image = ImageTk.PhotoImage(self.image)
        # self.background.configure(image =  self.background_image)
    def new_game(self):
        print("hi there, everyone!")

app = Application()
app.mainloop()