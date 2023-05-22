

class GameField:
    def __init__(self, screen, file, color1, color2):
        self.screen = screen
        self.file = file
        self.color_field = color1
        self.color_lives = color2

        self.map_matrix()
        self.init_field()

    def map_matrix(self):
        self.matrix = []
        with open(self.file, encoding="utf-8") as file:
            for line in file:
                self.matrix.append(list(line)[:-1])

    def init_field(self):  # создание окон
        hight, width = self.screen.getmaxyx()  # размер консоли (локальные переменные)
        m = self.matrix
        self.mh, self.mw = len(m), len(m[0])  # размер матрицы (атрибуты)

        offset_y = (hight - self.mh) // 2  # координаты сдвига
        offset_x = (width - self.mw) // 2

        self.mapa = self.screen.derwin(self.mh, self.mw, offset_y, offset_x)

        self.mapa.keypad(1)
        self.mapa.timeout(100)

        self.border = self.screen.derwin(
            self.mh + 4, self.mw + 8, offset_y - 2, offset_x - 4
        )

        self.border.box()
        self.border.refresh()

    def draw_field(self):
        for i, row in enumerate(self.matrix):
            for j, char in enumerate(row):
                if self.matrix[i][j] == "█" or self.matrix[i][j] == "-":
                    self.mapa.addstr(i, j, char, self.color_field)
                else:
                    self.mapa.addstr(i, j, char)

    def score_update(self, score):
        self.border.addstr(self.mh + 3, 20, "[ Score: {0} ]".format(score))
        self.border.refresh()

    def lives_update(self, lives):
        heart_str = "\u2665 " * lives

        line = "[ {0}]─────".format(heart_str)
        self.border.addstr(self.mh + 3, 35, line)

        self.border.addstr(self.mh + 3, 37, heart_str, self.color_lives)
        self.border.refresh()
