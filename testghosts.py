from objects.ghosts import Ghosts
import pytest

class Field():
    def __init__ (self):
        self.matrix = [
        [' ', ' ', '█', ' ', ' ', ' ', ' '],
        ['█', ' ', ' ', ' ', '█', ' ', ' '],
        [' ', ' ', '█', ' ', ' ', '█', '█'],
        [' ', ' ', ' ', ' ', ' ', ' ', ' '],
    ]

def test_update_position():
    field = Field()
    ghost = Ghosts(field, (1, 1), None)

    # Пустые
    assert ghost.update_position(1, 1, 'UP') == (0, 1)
    assert ghost.update_position(1, 1, 'DOWN') == (2, 1)
    assert ghost.update_position(1, 2, 'LEFT') == (1, 1)
    assert ghost.update_position(1, 1, 'RIGHT') == (1, 2)

    # Переход
    assert ghost.update_position(1, 0, 'LEFT') == (1, 6)
    assert ghost.update_position(1, 6, 'RIGHT') == (1, 1)

    # Столкновение
    assert ghost.update_position(3, 2, 'UP') == (3, 2)
    assert ghost.update_position(0, 4, 'DOWN') == (0, 4)
    assert ghost.update_position(2, 3, 'LEFT') == (2, 3)
    assert ghost.update_position(2, 1, 'RIGHT') == (2, 1)