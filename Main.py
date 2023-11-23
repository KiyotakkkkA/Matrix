import pygame as pg
import random as r
from numba import njit

pg.init()

run = True

DISPLAY_WIDTH = 1820
DISPLAY_HEIGHT = 900

normal_colors = ['green']
light_colors = ['lightgreen']
dark_colors = ['darkgreen']

clock = pg.time.Clock()
FPS = 60

katakana = (chr(i) for i in range(65, 91))
katakana2 = (chr(i) for i in range(65, 91))
katakana3 = (chr(i) for i in range(65, 91))

font = pg.font.Font('katakana.ttf', 30)
green_katakana = [font.render(char, True, pg.Color(r.choice(normal_colors))) for char in katakana]
light_green_katakana = [font.render(char, True, pg.Color(r.choice(light_colors))) for char in katakana2]
dark_green_katakana = [font.render(char, True, pg.Color(r.choice(dark_colors))) for char in katakana3]

columns_array = []
column_x = 10

window = pg.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
surf = pg.Surface((DISPLAY_WIDTH, DISPLAY_HEIGHT))
surf.set_alpha(100)


class Symbol:
    def __init__(self, x, y, type="standart"):
        self.x = x
        self.y = y
        self.size = 80
        self.speed = 1
        self.type = type
        self.interval = r.randrange(5, 30)
        self.value = None
        if self.type == "standart":
            self.value = r.choice(green_katakana + dark_green_katakana)
        elif self.type == "light":
            self.value = r.choice(light_green_katakana)

    def render(self, symbol):
        frames = pg.time.get_ticks()
        if not frames % self.interval:
            self.value = r.choice(symbol)
        window.blit(self.value, (self.x, self.y))

    def move(self, speed=None):
        if speed is None:
            self.y += self.speed
            if self.y >= DISPLAY_HEIGHT - self.size // 2:
                self.y = 10
        else:
            self.y += speed
            if self.y >= DISPLAY_HEIGHT - self.size // 2:
                self.y = 10


class SymbolsColumn:
    def __init__(self, y, number, speed, x=r.randint(10, DISPLAY_WIDTH - 10)):
        self.y = y
        self.x = x
        self.number = number
        self.array = []
        self.speed = speed

        self.create()

    def create(self):
        self.array.append(Symbol(self.x, self.y, type="light"))
        self.y -= 30

        for j1 in range(self.number - 1):
            self.array.append(Symbol(self.x, self.y))
            self.y -= 30

    def move_column(self):
        for i2 in self.array:
            if i2.type == "standart":
                i2.render(green_katakana + dark_green_katakana)
            elif i2.type == "light":
                i2.render(light_green_katakana)

            i2.move(self.speed)


for i in range(DISPLAY_WIDTH // 20):
    columns_array.append(SymbolsColumn(r.randrange(-DISPLAY_HEIGHT, 0), r.randint(13, 20), r.randint(1, 2), x=column_x))
    column_x += 20

while run:
    for i in pg.event.get():
        if i.type == pg.QUIT:
            quit()

    window.blit(surf, (0, 0))
    surf.fill(pg.Color('black'))

    for j2 in columns_array:
        j2.move_column()

    clock.tick(120)
    pg.display.flip()
