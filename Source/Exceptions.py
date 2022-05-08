__all__ = [
    'GameError',
    'MinesNumberError',
    'HeightError',
    'WidthError',
    'CellError',
    'WrongCellTypeError',
    'CellNumberNotProvided',
]


class GameError(Exception):
    ...


class MinesNumberError(GameError):
    ...


class HeightError(GameError):
    ...


class WidthError(GameError):
    ...


class CellError(GameError):
    ...


class WrongCellTypeError(CellError):
    ...


class CellNumberNotProvided(CellError):
    ...
