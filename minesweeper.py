from Source.minesweeper import Minesweeper, GameMode


def main():
    game = Minesweeper(game_mode=GameMode.hard)
    game.start_game()


if __name__ == '__main__':
    main()
