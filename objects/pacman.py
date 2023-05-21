import curses


class Pacman:
    def __init__(self, field, position, color):
        self.y, self.x = position
        self.field = field
        self.color = color
        self.prev_y = self.y
        self.prev_x = self.x

        self.pacman_symbols = {"UP": "v", "DOWN": "^", "LEFT": ">", "RIGHT": "<"}

    def move(self, direction):
        self.prev_y = self.y  # сохраняем текущие координаты
        self.prev_x = self.x
        direct = direction

        if direct == "UP":
            self.y -= 1
        elif direct == "DOWN":  # изменяем координаты в соответствии с направлением
            self.y += 1
        elif direct == "LEFT":
            self.x -= 1
        elif direct == "RIGHT":
            self.x += 1

        width = len(self.field.matrix[0])  # проход
        if self.x < 0:
            self.x = width - 1  # влево
        elif self.x >= width - 1:  # вправо
            self.x = 1

        if (
            self.field.matrix[self.y][self.x] == "█"
            or self.field.matrix[self.y][self.x] == "-"
        ):  # если новые координаты - стена, возвращаем первоначальные
            self.y = self.prev_y
            self.x = self.prev_x
            # self.stopped = True
        else:
            self.draw(
                self.prev_y, self.prev_x, direction
            )  # если не стена -> нужно отрисовать в новых координатах и стереть из предыдущих

    def set_character(self, position):
        self.disappear()
        self.y, self.x = position
        direction = "RIGHT"
        self.field.mapa.addch(
            self.y, self.x, self.pacman_symbols[direction], self.color
        )

        self.field.mapa.refresh()

    def disappear(self):
        clear = " "
        self.field.mapa.addch(self.y, self.x, clear)
        self.field.mapa.refresh()

    def draw(self, prev_y, prev_x, direction):
        clear = " "

        self.field.mapa.addch(  # стираем пакмана с предыдущей позиции
            prev_y, prev_x, clear
        )

        self.field.mapa.addch(  # рисуем на новой
            self.y, self.x, self.pacman_symbols[direction], self.color
        )

        self.field.mapa.refresh()
