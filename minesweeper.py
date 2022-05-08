from Source import (
    Minesweeper,
    GameMode,
    Const,
)
import argparse

GAME_MODE_MAPPING = {
    'easy': GameMode.easy,
    'normal': GameMode.normal,
    'hard': GameMode.hard,
    'custom': GameMode.custom,
}


def main():
    game = Minesweeper(game_mode=GAME_MODE, mines_count=MINES_COUNT, height=HEIGHT, width=WIDTH)
    game.start_game()


if __name__ == '__main__':
    # ArgParser init
    ArgParser = argparse.ArgumentParser()
    ArgParser.add_argument(
        '-g', '--game-mode',
        choices=list(GAME_MODE_MAPPING),
        default='easy',
        help='Game mode',
    )
    ArgParser.add_argument(
        '--height',
        choices=range(Const.Game.min_height, Const.Game.max_height + 1),
        metavar=f'[{Const.Game.min_height}-{Const.Game.max_height}]',
        help='Cells in column',
    )
    ArgParser.add_argument(
        '--width',
        choices=range(Const.Game.min_width, Const.Game.max_width + 1),
        metavar=f'[{Const.Game.min_width}-{Const.Game.max_width}]',
        help='Cells in row',
    )
    ArgParser.add_argument(
        '--mines-count',
        choices=range(Const.Game.min_mines_count, Const.Game.max_mines_count + 1),
        metavar=f'[{Const.Game.min_mines_count}-{Const.Game.max_mines_count}]',
        help='Mines on field',
    )
    ArgParser.add_argument('--debug', action='store_true', help='Debug')

    # Parsing args
    ScriptArgs = ArgParser.parse_args()
    GAME_MODE = GAME_MODE_MAPPING[ScriptArgs.game_mode]
    HEIGHT = ScriptArgs.height
    WIDTH = ScriptArgs.width
    MINES_COUNT = ScriptArgs.mines_count
    DEBUG = ScriptArgs.debug

    # Main
    main()
