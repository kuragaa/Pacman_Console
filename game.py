import curses
from objects.pacman import Pacman
from objects.field import GameField
from objects.ghosts import Ghosts
import colorinit
import time

DATA = {
    "map_file": "maps/map.txt",
    "start": "screens/start.txt",
    "win": "screens/win.txt",
    "end": "screens/gameover.txt",
    "character_positions": {
        "pacman": [18, 29],
        "ghosts": [[11, 25], [11, 26], [11, 28], [11, 29]],
    },
}


class PacmanGame:
    def __init__(self):
        self.screen = curses.initscr()
        curses.curs_set(0)
        curses.noecho()

        self.init_field()
        self.start_screen()

    def init_field(self):
        self.field = GameField(
            self.screen, DATA["map_file"], curses.color_pair(4), curses.color_pair(1)
        )

    def init_characters(self):
        positions = DATA["character_positions"]
        ghosts = positions["ghosts"]

        self.pacman = Pacman(self.field, positions["pacman"], curses.color_pair(3))
        self.ghosts = {
            "Green": Ghosts(self.field, ghosts[0], curses.color_pair(2)),
            "Red": Ghosts(self.field, ghosts[1], curses.color_pair(1)),
            "Pink": Ghosts(self.field, ghosts[2], curses.color_pair(5)),
            "Blue": Ghosts(self.field, ghosts[3], curses.color_pair(6)),
        }

    def new_game(self):
        self.lives = 3
        self.food = 267
        self.score = 0

        self.field.map_matrix()
        self.field.draw_field()
        self.field.lives_update(self.lives)
        self.field.score_update(self.score)
        self.init_characters()
        self.run_game()

    def run_game(self):
        game = True
        key = curses.KEY_RIGHT

        while game:
            next_key = self.field.mapa.getch()
            key = key if next_key == -1 else next_key

            for ghost in self.ghosts.values():
                ghost.move_random()

            if self.collision():
                game = False

                self.die()

                self.field.mapa.refresh()

                if self.lives > 0:
                    self.restart()
                else:
                    self.end_screen(DATA["end"])

            if self.eat_food():
                self.food -= 1
                self.inc_score()
                if self.food <= 0:
                    game = False
                    self.win()

            if key == curses.KEY_UP or key == ord("w") or key == ord("W"):
                self.pacman.move("UP")

            if key == curses.KEY_DOWN or key == ord("s") or key == ord("S"):
                self.pacman.move("DOWN")

            if key == curses.KEY_LEFT or key == ord("a") or key == ord("A"):
                self.pacman.move("LEFT")

            if key == curses.KEY_RIGHT or key == ord("d") or key == ord("D"):
                self.pacman.move("RIGHT")

            if key == 27:
                game = False
                curses.endwin()

    def eat_food(self):
        y = self.pacman.y
        x = self.pacman.x
        if self.field.matrix[y][x] == "·":
            self.field.matrix[y][x] = " "
            return True
        else:
            return False

    def inc_score(self):
        value = 10
        self.score += value
        self.field.score_update(self.score)

    def collision(self):
        for ghost in self.ghosts.values():
            if (ghost.y, ghost.x) in [
                (self.pacman.y, self.pacman.x),
                (self.pacman.prev_y, self.pacman.prev_x),
            ]:
                return True
        return False

    def die(self):
        self.lives -= 1
        self.field.lives_update(self.lives)

    def reset_positions(self):
        positions = DATA["character_positions"]
        ghosts = positions["ghosts"]

        self.pacman.set_character(positions["pacman"])

        for i, ghost in enumerate(self.ghosts.values()):
            ghost.set_character(ghosts[i])

    def restart(self):
        self.reset_positions()
        self.run_game()

    def start_screen(self):
        with open(DATA["start"], encoding="utf-8") as screen:
            lines = screen.readlines()
            for i, line in enumerate(lines):
                try:
                    if 7 <= i <= 15:
                        self.field.mapa.addstr(i, 0, line.rstrip())
                    else:
                        self.field.mapa.addstr(
                            i, 0, line.rstrip(), curses.color_pair(4)
                        )
                except curses.error:
                    pass

        self.field.mapa.refresh()
        self.field.border.refresh()

        run = True
        while run:
            next_key = self.field.mapa.getch()
            if next_key != -1:
                run = False
                self.new_game()
            time.sleep(0.5)

    def win(self):
        self.end_screen(DATA["win"])

    def end_screen(self, file):
        with open(file, encoding="utf-8") as screen:
            lines = screen.readlines()
            for i, line in enumerate(lines):
                try:
                    if "SCORE: 0000" in line:
                        line = line.replace(
                            "SCORE: 0000", "SCORE: " + str(self.score).zfill(4)
                        )
                    if 7 <= i <= 15:
                        self.field.mapa.addstr(i, 0, line.rstrip())
                    else:
                        self.field.mapa.addstr(
                            i, 0, line.rstrip(), curses.color_pair(4)
                        )
                except curses.error:
                    pass

            i = 0
            for line in lines:
                j = 0
                for char in line:
                    if char == "\u2665":
                        self.field.mapa.addch(i, j, char, curses.color_pair(1))
                    j += 1
                i += 1

        self.field.mapa.refresh()
        self.field.border.refresh()

        run = True
        while run:
            next_key = self.field.mapa.getch()
            if next_key != -1:
                run = False
                if next_key == 27:
                    curses.endwin()
                else:
                    self.field.mapa.clear()
                    self.new_game()


def main():
    PacmanGame()


if __name__ == '__main__':
    main()
