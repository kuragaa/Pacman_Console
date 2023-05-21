import curses
import random


class Ghosts:
    def __init__(self, field, position, color):
        self.field = field
        self.y, self.x = position
        self.color = color
        self.symbol = "M"
        self.cur_direction = "RIGHT"

        self.init_directions()

    def init_directions(self):
        self.directions = ["UP", "DOWN", "LEFT", "RIGHT"]

    def opposite_direction(self, direction):
        opposite_direction = {
            "UP": "DOWN",
            "DOWN": "UP",
            "LEFT": "RIGHT",
            "RIGHT": "LEFT",
        }
        return opposite_direction[direction]

    def forward_directions(self, cur_direction):
        directions = self.directions[:]
        directions.remove(self.opposite_direction(cur_direction))
        return directions

    def set_character(self, position):
        self.disappear()
        self.y, self.x = position
        direction = "RIGHT"
        self.field.mapa.addch(self.y, self.x, self.symbol, self.color)

        self.field.mapa.refresh()

    def disappear(self):
        clear = " "
        self.field.mapa.addch(self.y, self.x, clear)
        self.field.mapa.refresh()

    def update_position(self, y, x, direction):  # не изменяет атрибуты
        prev_y = y
        prev_x = x

        new_y = y
        new_x = x

        if direction == "UP":
            new_y -= 1
        elif direction == "DOWN":
            new_y += 1
        elif direction == "LEFT":
            new_x -= 1
        elif direction == "RIGHT":
            new_x += 1

        width = len(self.field.matrix[0])  # проход
        if new_x < 0:
            new_x = width - 1  # влево
        elif new_x >= width - 1:  # вправо
            new_x = 1

        if (
            self.field.matrix[new_y][new_x] == "█"
        ):  # если новые координаты - стена, возвращаем первоначальные
            return prev_y, prev_x
        else:
            return new_y, new_x

    def move(self):  # изменяет атрибуты
        prev_y, prev_x = self.y, self.x
        self.y, self.x = self.update_position(self.y, self.x, self.cur_direction)

        clear = " "
        if self.field.matrix[prev_y][prev_x] == "-":
            self.field.mapa.addch(prev_y, prev_x, clear)  # стираем с предыдущей позиции

            self.field.mapa.addch(prev_y, prev_x, "-")  # стираем с предыдущей позиции

        elif self.field.matrix[prev_y][prev_x] == "·":
            self.field.mapa.addch(prev_y, prev_x, clear)

            self.field.mapa.addch(prev_y, prev_x, "·")  # стираем с предыдущей позиции

        else:
            self.field.mapa.addch(prev_y, prev_x, clear)

        self.field.mapa.addch(  # рисуем на новой
            self.y, self.x, self.symbol, self.color
        )

        self.field.mapa.refresh()

    def move_random(self):
        cur_y = self.y  # текущие
        cur_x = self.x
        cur_direction = self.cur_direction

        forward_directions = self.forward_directions(
            cur_direction
        )  # возможные направления вперед, после текущего направления
        possible_directions = []

        for (
            i
        ) in (
            forward_directions
        ):  # вычисляем, какие направления вперед возможны (если нет препятствий)
            if self.update_position(cur_y, cur_x, i) != (
                self.y,
                self.x,
            ):  # вычисляем возможность шага !!!без изменения текущих данных!!!
                possible_directions.append(i)  # массив возможных направлений

        if possible_directions:  # если есть куда идти (не противоположное)
            self.cur_direction = random.choice(possible_directions)
            self.move()  # двигаемся в рандомном из возможных, изменяем текущее направление и текщие координаты

        else:
            self.cur_direction = self.opposite_direction(cur_direction)
            self.move()
