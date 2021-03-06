from enum import Enum

__all__ = ['GameMode', 'Const']


class GameMode(Enum):
    """
    Game modes
    """
    easy = 'Easy'
    normal = 'Normal'
    hard = 'Hard'
    custom = 'Custom'


class Const:
    """
    Constants
    """
    class Game:
        """
        Game
        """
        name = 'Minesweeper'
        frame_rate = 60
        modes = {
            GameMode.easy: {
                'mines_count': 10,
                'size': 9,
            },
            GameMode.normal: {
                'mines_count': 40,
                'size': 16,
            },
            GameMode.hard: {
                'mines_count': 99,
                'size': 22,  # 30 * 16
            },
        }
        min_mines_count = 10
        max_mines_count = 200
        min_height = 9
        max_height = 100
        min_width = 9
        max_width = 100

    class Color:
        """
        Colors
        """
        # Default colors
        black = (0, 0, 0)
        white = (255, 255, 255)
        red = (255, 0, 0)
        green = (0, 255, 0)
        yellow = (255, 255, 0)

        background = (211, 235, 204)
        menu = (128, 128, 128)
        menu_block = black
        cell_hidden = (150, 150, 150)
        cell_opened = (133, 218, 237)
        cell_flagged = yellow
        cell_mine = black

    class Size:
        """
        Sizes, spaces
        """
        space = 6
        cell_space = 2
        cell = 20
        menu_height = 60
        menu_block_width = 60
        menu_block_height = 40
        start_button = 40

    class Font:
        """
        Font
        """
        cell = None
        cell_size = 18
        menu = None
        menu_size = 30
